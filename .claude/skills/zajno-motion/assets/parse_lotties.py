#!/usr/bin/env python3
"""Parse Zajno's Lottie JSON files and extract empirical animation data.

Lottie schema reference:
  - "fr": framerate (fps)
  - "ip": in-point (start frame)
  - "op": out-point (end frame)  -> duration = (op - ip) / fr seconds
  - "w","h": composition size
  - "layers": layer array
  - "k": keyframes — either a list of dicts (animated) or a single value (static)
  - Each keyframe dict has: "t" (time/frame), "s" (start value), optional "i"/"o" (bezier in/out tangents)
  - "i" and "o" are dicts with "x" and "y" arrays — these are the cubic-bezier control points
  - Colors appear in shape fills as "c.k" — RGBA normalized to 0..1
"""

import json, os, sys
from pathlib import Path
from collections import Counter, defaultdict

LOTTIE_DIR = Path.home() / ".cache/zajno-motion/lotties"

# ─── Collectors ────────────────────────────────────────────────────────
colors = Counter()                  # (r,g,b,a) → count
easings = Counter()                 # (ix, iy, ox, oy) rounded → count
durations = []                      # per-file (filename, duration_s, fr, frames, layers, size_bytes)
all_durations_s = []                # for histogram
framerates = Counter()              # fr → count
layer_counts = Counter()            # n_layers bucketed
keyframe_count_per_file = []        # avg keyframes per layer
total_keyframes = 0
animated_props = 0

def walk(node, on_keyframe=None, on_color=None):
    """Walk arbitrary nested Lottie JSON, firing callbacks."""
    if isinstance(node, dict):
        # Detect a "k" (keyframe array or static value) inside an animation property
        # An animated property has "a": 1 and "k": [list of keyframe dicts]
        if node.get("a") == 1 and isinstance(node.get("k"), list):
            for kf in node["k"]:
                if isinstance(kf, dict) and on_keyframe:
                    on_keyframe(kf)
        # Color property: "ty":"fl" (fill) contains "c" which is a property with "k" = [r,g,b,a]
        # OR animated color with "k" = list of keyframes whose "s" is [r,g,b,a]
        if "c" in node and isinstance(node["c"], dict):
            c = node["c"]
            if c.get("a") == 0 and isinstance(c.get("k"), list) and len(c["k"]) >= 3:
                if on_color: on_color(c["k"])
            elif c.get("a") == 1 and isinstance(c.get("k"), list):
                for kf in c["k"]:
                    if isinstance(kf, dict) and isinstance(kf.get("s"), list) and len(kf["s"]) >= 3:
                        if on_color: on_color(kf["s"])
        for v in node.values():
            walk(v, on_keyframe, on_color)
    elif isinstance(node, list):
        for v in node:
            walk(v, on_keyframe, on_color)

def rgb_to_hex(rgba):
    r, g, b = (max(0, min(255, int(round(c * 255)))) for c in rgba[:3])
    return f"#{r:02x}{g:02x}{b:02x}"

def luminance(rgba):
    r, g, b = rgba[:3]
    return 0.2126*r + 0.7152*g + 0.0722*b

def analyze_file(path: Path):
    global total_keyframes, animated_props
    try:
        data = json.loads(path.read_text())
    except Exception as e:
        print(f"SKIP {path.name}: {e}", file=sys.stderr)
        return

    fr = data.get("fr", 0)
    ip = data.get("ip", 0)
    op = data.get("op", 0)
    duration_s = (op - ip) / fr if fr else 0
    layers = data.get("layers", [])
    n_layers = len(layers)
    size_b = path.stat().st_size

    framerates[fr] += 1
    layer_counts[n_layers] += 1
    durations.append((path.name, round(duration_s, 2), fr, op - ip, n_layers, size_b))
    if duration_s > 0:
        all_durations_s.append(duration_s)

    file_keyframes = 0
    def on_kf(kf):
        nonlocal file_keyframes
        global total_keyframes
        file_keyframes += 1
        total_keyframes += 1
        # Easing bezier — i (in-tangent) and o (out-tangent), each with x[] and y[]
        i = kf.get("i", {})
        o = kf.get("o", {})
        ix = i.get("x"); iy = i.get("y")
        ox = o.get("x"); oy = o.get("y")
        if all(isinstance(v, list) and v for v in (ix, iy, ox, oy)):
            # GSAP-style cubic-bezier is (ox[0], oy[0], 1-ix[0], 1-iy[0])
            # but Lottie's i/o are control points for the segment;
            # we'll just round and count the (ox, oy, ix, iy) quadruple
            try:
                tup = (round(ox[0], 3), round(oy[0], 3), round(ix[0], 3), round(iy[0], 3))
                easings[tup] += 1
            except Exception:
                pass

    def on_color(rgba):
        if len(rgba) >= 3:
            colors[rgb_to_hex(rgba)] += 1

    walk(data, on_kf, on_color)
    keyframe_count_per_file.append((path.name, file_keyframes, n_layers))

# ─── Run ─────────────────────────────────────────────────────────────
files = sorted(LOTTIE_DIR.glob("*.json"))
print(f"Parsing {len(files)} Lottie files from {LOTTIE_DIR}", file=sys.stderr)

for f in files:
    analyze_file(f)

# ─── Output ──────────────────────────────────────────────────────────
out = {
    "files_analyzed": len(files),
    "total_keyframes": total_keyframes,
    "framerates": dict(framerates),
    "duration_histogram": {
        "min_s": round(min(all_durations_s), 2) if all_durations_s else 0,
        "max_s": round(max(all_durations_s), 2) if all_durations_s else 0,
        "median_s": round(sorted(all_durations_s)[len(all_durations_s)//2], 2) if all_durations_s else 0,
        "mean_s": round(sum(all_durations_s)/len(all_durations_s), 2) if all_durations_s else 0,
    },
    "layer_counts_distribution": dict(layer_counts),
    "top_easings": [
        {"ox": o[0], "oy": o[1], "ix": o[2], "iy": o[3], "uses": c}
        for o, c in easings.most_common(20)
    ],
    "top_colors": [
        {"hex": h, "uses": c, "luminance": round(luminance(tuple(int(h[i:i+2],16)/255 for i in (1,3,5))), 3)}
        for h, c in colors.most_common(30)
    ],
    "per_file": [
        {"name": n, "duration_s": d, "fr": f, "frames": fl, "layers": ly, "bytes": b}
        for (n, d, f, fl, ly, b) in sorted(durations, key=lambda x: -x[5])
    ],
}

print(json.dumps(out, indent=2))
