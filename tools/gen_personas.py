"""
Persona art generation: Seonso and Grumpy Carrot, alive on the Dreamland.

Uses the same OpenRouter (Gemini image) pipeline as tools/gen.py, with one
difference that matters: the style reference is each PERSONA's own sheet, not
the studio logo. The personas each have their own distinct style, deliberately
(PROJECT.md, brand/characters/PERSONA_PALETTES.md), so their art is drawn in
their style, not the studio's.

Each pose is generated twice, so the blink is drawn art and never faked:

  1. <pose>.png          eyes open, on a flat cream plate, then cut out
  2. <pose>_closed.png   the SAME image sent back with one instruction:
                         close the eyes, change nothing else
  3. <pose>_blink.png    only the region that changed between 1 and 2 (the
                         eyes), cut out of the closed frame and saved with its
                         offset, so the site can swap it in for ~150ms
  4. <pose>_blink.json   where that patch sits on the base image, in percent

The key is read from OPENROUTER_API_KEY / OPENAI_API_KEY or a gitignored .env,
exactly as tools/gen.py does. It is never printed, logged or written anywhere.
openrouter.ai must be reachable from the environment.

Usage
  python tools/gen_personas.py --list
  python tools/gen_personas.py --dry-run
  python tools/gen_personas.py --only duo-cloud --model flash   # cheap draft
  python tools/gen_personas.py --only duo-cloud                 # best quality
  python tools/gen_personas.py --blink-only --only duo-cloud    # redo the diff
"""

import argparse
import base64
import io
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402  (shared key reading, API call shape, cream matte)

ROOT = gen.ROOT
CHAR = ROOT / "brand" / "characters"
SEONSO_REFS = [CHAR / "seonso" / "seonso_ref_sheet.jpeg", CHAR / "seonso" / "seonso_ref_sheet_v2.jpeg"]
GRUMPY_REFS = [CHAR / "grumpy-carrot" / "grumpy_carrot_ref_sheet_corrected.jpeg"]
CLOUD_REF = ROOT / "art-masters" / "dream" / "island-base.png"

MASTERS = ROOT / "art-masters" / "personas"
OUT = ROOT / "site" / "public" / "images" / "personas"

# Who they are, from the brand files. Colours are their own palettes
# (PERSONA_PALETTES.md), never the studio tokens.
SEONSO = (
    "SEONSO (the first attached character sheets): a chibi fox-sage artist. Black "
    "hair tied up in a bun with a gold hairpin and tassel, gentle brown eyes, "
    "light stubble, a black-and-gold patterned jacket over a cream hoodie with a "
    "spiral mark, black trousers, white sneakers. Calm and mindful. His "
    "companion is a small white fox spirit with many soft tails and a gold "
    "spiral mark on its forehead."
)
GRUMPY = (
    "GRUMPY CARROT (the next attached character sheet): a chibi bunny-girl artist. "
    "Long wavy light-brown hair, tall white-and-pink bunny ears, orange carrot "
    "hair clips with green leaves, big green eyes, a pink hoodie under a black "
    "apron with pockets holding pens, black stockings with bunny faces, pink "
    "sneakers. Cute, a little grumpy, secretly a softie. Never add the text "
    "'I hate Mondays' anywhere."
)

STYLE = (
    "Draw them exactly in the art style of their attached character sheets: soft "
    "painted chibi illustration, big expressive eyes, gentle shading, clean "
    "linework, the same faces, outfits and proportions as the sheets. They must "
    "be instantly recognisable as the same characters. Soft, warm, dreamy "
    "daylight. No text, no letters, no logos, no speech bubbles, no watermark, "
    "no border."
)

PLATE = (
    "IMPORTANT: place everything on a completely flat, uniform, solid cream "
    "#F4EDD8 background. The background must be one single flat colour with no "
    "gradient, no texture, no ground shadow, no floor, no vignette and no "
    "frame. The characters must be COMPLETE and fully inside the frame with "
    "generous empty cream space on every side: nothing cropped by the edge."
)

CLOSE_EYES = (
    "Edit this image. Change ONLY the eyes: make every character's eyes gently "
    "closed, drawn as soft calm closed-eye curves in the same art style, as if "
    "mid-blink. Keep absolutely everything else identical: the same pose, "
    "position, framing, size, colours, hair, outfit, background and lighting, "
    "pixel for pixel. Do not move, redraw or restyle anything except the eyes."
)

POSES = {
    "duo-cloud": dict(
        refs=SEONSO_REFS + GRUMPY_REFS + [CLOUD_REF], aspect="4:3",
        prompt=f"{SEONSO}\n\n{GRUMPY}\n\nSeonso and Grumpy Carrot sit side by side "
        "on top of a small soft floating cloud (shaped like the attached cloud "
        "reference: a plump rounded cushion of pale cream cloud with a wispy "
        "underside). Their legs dangle over the front edge. They look relaxed and "
        "happy, facing the viewer, eyes open. Seonso's white fox spirit curls up "
        "on the cloud beside him. Full bodies visible, centred."),
    "duo-peek": dict(
        refs=SEONSO_REFS + GRUMPY_REFS + [CLOUD_REF], aspect="16:9",
        prompt=f"{SEONSO}\n\n{GRUMPY}\n\nSeonso and Grumpy Carrot peek up over the "
        "top edge of a soft billowing bank of pale cream cloud: only their heads, "
        "shoulders and hands are visible above the cloud, hands resting on it. "
        "They look up and slightly toward the viewer with curious, delighted "
        "faces, eyes open. Grumpy Carrot's bunny ears stand tall. The cloud bank "
        "runs across the whole bottom of the frame."),
    "seonso-stand": dict(
        refs=SEONSO_REFS, aspect="3:4",
        prompt=f"{SEONSO}\n\nSeonso alone, standing, full body, three-quarter view, "
        "holding a brush in one hand and his sketchbook in the other, a gentle "
        "welcoming smile, eyes open. His white fox spirit sits at his feet."),
    "grumpy-stand": dict(
        refs=GRUMPY_REFS, aspect="3:4",
        prompt=f"{GRUMPY}\n\nGrumpy Carrot alone, standing, full body, three-quarter "
        "view, holding a pen in one hand and her pink bunny sketchbook in the "
        "other, a small pout that is secretly a smile, eyes open. Her whole hair "
        "and both ears fully visible."),
}


def data_uri(path: Path) -> str:
    """Encode a reference for the API. RGBA art is flattened onto the cream
    plate first, so the model sees it the way it is asked to paint."""
    from PIL import Image
    im = Image.open(path)
    if im.mode in ("RGBA", "LA"):
        bg = Image.new("RGBA", im.size, (244, 237, 216, 255))
        bg.alpha_composite(im.convert("RGBA"))
        im = bg
    buf = io.BytesIO()
    im.convert("RGB").save(buf, "JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def call(key, model, prompt, images, aspect=None):
    content = [{"type": "text", "text": prompt}]
    content += [{"type": "image_url", "image_url": {"url": u}} for u in images]
    body = {"model": model, "modalities": ["image", "text"],
            "messages": [{"role": "user", "content": content}]}
    if aspect:
        body["image_config"] = {"aspect_ratio": aspect}
    req = urllib.request.Request(
        gen.API, data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                 "X-Title": "Midori Fuwafuwa personas"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def build_prompt(spec):
    return f"{STYLE}\n\n{spec['prompt']}\n\n{PLATE}"


def blink_patch(name, pad=6, thresh=38):
    """Cut the eyes out of the closed frame.

    Diff the open and closed plates, keep only the changed regions that sit
    in the upper part of each figure (eyes, not stray noise), pad them, and
    save that patch from the closed frame with its position. If the model
    moved anything else, the diff grows past a sane size and we say so rather
    than ship a patch that would jump.
    """
    import numpy as np
    from PIL import Image
    from scipy import ndimage

    op = Image.open(MASTERS / f"{name}_raw.png").convert("RGB")
    cl = Image.open(MASTERS / f"{name}_closed_raw.png").convert("RGB")
    if cl.size != op.size:
        cl = cl.resize(op.size, Image.LANCZOS)
    a = np.asarray(op).astype(int)
    b = np.asarray(cl).astype(int)
    diff = np.abs(a - b).max(axis=2) > thresh
    diff = ndimage.binary_opening(diff, iterations=1)
    lab, n = ndimage.label(ndimage.binary_dilation(diff, iterations=4))
    if n == 0:
        print(f"  {name}: no difference found; the eyes did not change")
        return
    sizes = ndimage.sum(diff, lab, range(1, n + 1))
    keep = [i + 1 for i, s in enumerate(sizes) if s > 40]
    mask = np.isin(lab, keep)
    ys, xs = np.where(mask)
    x0, y0 = max(xs.min() - pad, 0), max(ys.min() - pad, 0)
    x1, y1 = min(xs.max() + pad, op.width), min(ys.max() + pad, op.height)
    area = (x1 - x0) * (y1 - y0) / (op.width * op.height)
    if area > 0.12:
        print(f"  {name}: WARNING the closed frame changed {area:.0%} of the image, "
              "not just the eyes. Regenerate the closed frame before using it.")
    # soft-edged patch from the closed frame, masked to the changed area
    soft = ndimage.gaussian_filter(ndimage.binary_dilation(mask, iterations=3).astype(float), 2)
    patch = Image.fromarray(np.dstack([b, (soft * 255).clip(0, 255)]).astype("uint8"), "RGBA")
    patch = patch.crop((x0, y0, x1, y1))
    patch.save(MASTERS / f"{name}_blink.png", optimize=True)
    OUT.mkdir(parents=True, exist_ok=True)
    patch.save(OUT / f"{name}_blink.webp", "WEBP", quality=92, method=6)
    pos = {"left": round(float(x0) / op.width * 100, 3), "top": round(float(y0) / op.height * 100, 3),
           "width": round(float(x1 - x0) / op.width * 100, 3), "height": round(float(y1 - y0) / op.height * 100, 3)}
    (MASTERS / f"{name}_blink.json").write_text(json.dumps(pos, indent=2))
    (OUT / f"{name}_blink.json").write_text(json.dumps(pos, indent=2))
    print(f"  blink patch {name}: {pos} ({area:.1%} of the image)")


def save(name, png_bytes, suffix=""):
    from PIL import Image
    MASTERS.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    raw = Image.open(io.BytesIO(png_bytes))
    raw.convert("RGB").save(MASTERS / f"{name}{suffix}_raw.png", optimize=True)
    im = gen.matte_cream(raw)
    im.save(MASTERS / f"{name}{suffix}.png", optimize=True)
    im.save(OUT / f"{name}{suffix}.webp", "WEBP", quality=90, method=6)
    print(f"  saved {name}{suffix} {im.size}")
    return png_bytes


def first_image(resp, what):
    imgs = gen.extract_images(resp)
    if imgs:
        return imgs[0]
    txt = ""
    try:
        txt = resp["choices"][0]["message"].get("content") or ""
    except Exception:
        pass
    print(f"  no image returned for {what}. {str(txt)[:300]}")
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", action="append")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--model", default="pro", choices=list(gen.MODELS))
    ap.add_argument("--open-only", action="store_true", help="skip the closed-eye frame")
    ap.add_argument("--blink-only", action="store_true", help="redo the blink patch from saved plates; no API calls")
    args = ap.parse_args()

    names = args.only or list(POSES)
    bad = [n for n in names if n not in POSES]
    if bad:
        sys.exit(f"unknown pose(s): {', '.join(bad)}\nknown: {', '.join(POSES)}")
    if args.list:
        print("\n".join(names))
        return
    missing = [str(p) for n in names for p in POSES[n]["refs"] if not p.exists()]
    if missing:
        sys.exit("missing reference files:\n  " + "\n  ".join(missing))
    if args.dry_run:
        for n in names:
            refs = ", ".join(p.name for p in POSES[n]["refs"])
            print(f"\n===== {n}  (aspect {POSES[n]['aspect']}; refs: {refs}) =====\n{build_prompt(POSES[n])}")
        print(f"\n===== closed-eye edit (sent with each generated image) =====\n{CLOSE_EYES}")
        per = 2 if not args.open_only else 1
        print(f"\n{len(names) * per} image calls. ~$0.13-0.24 each on 'pro', ~$0.03 on 'flash'.")
        return
    if args.blink_only:
        for n in names:
            blink_patch(n)
        return

    key = gen.read_key()
    if not key:
        sys.exit("No API key found (env OPENROUTER_API_KEY / OPENAI_API_KEY, or .env).")
    model = gen.MODELS[args.model]
    print(f"model: {model}")
    for n in names:
        spec = POSES[n]
        print(f"\n>> {n}")
        try:
            refs = [data_uri(p) for p in spec["refs"]]
            base = first_image(call(key, model, build_prompt(spec), refs, spec["aspect"]), n)
            if not base:
                continue
            save(n, base)
            if args.open_only:
                continue
            shown = "data:image/png;base64," + base64.b64encode(base).decode()
            closed = first_image(call(key, model, CLOSE_EYES, [shown], spec["aspect"]), f"{n} closed")
            if not closed:
                continue
            save(n, closed, "_closed")
            blink_patch(n)
        except urllib.error.HTTPError as e:
            print(f"  HTTP {e.code}: {e.read().decode()[:300]}")
        except Exception as e:
            print(f"  FAILED: {type(e).__name__}: {e}")
    print(f"\nDone. Masters in {MASTERS}, web art in {OUT}")


if __name__ == "__main__":
    main()
