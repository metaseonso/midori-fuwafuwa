"""
Dreamland art generation — OpenRouter (Gemini image models).

Generates the layered parallax art for the studio site in the logo's own
painted style, sending the official logo as a style reference image.

  Style source of truth: brand/logo/midori_fuwafuwa_logo_official.png
  Palette:               brand/DESIGN_SYSTEM.md  §1 (nothing outside it)

Transparency: these models do not reliably emit an alpha channel, so each
layer is generated as light art on a pure black plate and the matte is
pulled from luminance (alpha = luminance). That is the standard way to
matte soft, wispy subjects — it keeps feathered cloud edges intact, where
chroma-keying would leave a hard fringe.

The key is read from the environment or a gitignored .env. It is never
printed, logged, or written anywhere.

Usage
  python tools/gen.py --list
  python tools/gen.py --dry-run
  python tools/gen.py --only sky-near
  python tools/gen.py --only sky-near --model flash     # cheap iteration
  python tools/gen.py                                   # everything
"""

import argparse
import base64
import io
import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGO = ROOT / "brand" / "logo" / "midori_fuwafuwa_logo_official.png"
OUT = ROOT / "site" / "public" / "images" / "dream"
API = "https://openrouter.ai/api/v1/chat/completions"

MODELS = {
    "pro": "google/gemini-3-pro-image",     # best quality, ~$0.13-0.24/image
    "flash": "google/gemini-2.5-flash-image",  # cheap iteration, ~$0.03/image
}

# ---------------------------------------------------------------------------
# House style. Prepended to every prompt so all layers read as one world.
# DESIGN_SYSTEM §1 (palette) and §6 (illustration rules).
# ---------------------------------------------------------------------------
STYLE = (
    "Match the art style of the attached reference image exactly: soft-painted "
    "kawaii storybook illustration, airbrushed pastel gouache with gently "
    "blended shading, delicate soft edges, luminous and high-key. "
    "Absolutely no hard black outlines, no bold vector strokes, no cel shading, "
    "no flat graphic shapes. Dreamy, weightless, fluffy (fuwa-fuwa). "
    "Palette strictly limited to: cream #F4EDD8, mint #BEECCE, soft mint "
    "#D1EFDE, pale mint #EDF1EB, blush pink #F8D1D1, pale blush #FCF2F4, "
    "sage #748872, pale sage #DADBCE. Pale cream and near-white dominate; "
    "mint and blush appear only as gentle accents in the shadows and hollows. "
    "No text, no letters, no logo, no characters, no faces, no creatures."
)

# Light art on a black plate -> matte. See module docstring.
#
# The anti-fringe clause is load-bearing: told only "paint on black", the
# model reads "soft edge" and "fade out" as "fade to dark grey", which
# produces a dirty rim no matte can recover — the darkness is real paint,
# not plate contamination. It must be told the art stays pale to its edges.
PLATE = (
    "IMPORTANT: place the subject on a pure solid black (#000000) background "
    "with nothing else in the frame. The background must be perfectly black "
    "and completely empty. Do not add any border, frame, vignette, watermark, "
    "or ground shadow.\n"
    "CRITICAL: the artwork itself must stay pale, light and luminous all the "
    "way to its outermost edges. Never darken, grey, shade or fade any edge "
    "toward black or grey. No dark rim, no dark outline, no grey haze, no "
    "smoky or sooty edges, no drop shadow. Where the artwork ends it should "
    "simply stop against the black, still at its palest cream tone. Any "
    "shadow inside the artwork must be a soft pale mint or blush tint, never "
    "grey, brown or black."
)

# Cream plate. The model kept painting a dark ink rim whenever it was told
# to work on black — that darkness is real paint, so no matte can recover
# it (rembg fails on it too). Painting on the logo's own cream ground
# removes the cause: there is nothing dark to blend an edge into. The cut
# is then a border flood-fill, the same method that cleanly lifted the
# wordmark and mascot off the logo.
PLATE_CREAM = (
    "IMPORTANT: place the artwork on a completely flat, uniform, solid cream "
    "#F4EDD8 background, exactly like the background of the reference image. "
    "The background must be one single flat colour with no gradient, no "
    "texture, no vignette, no border and no frame. Do not paint any shadow, "
    "glow, haze or dark edge where the artwork meets the background — the "
    "artwork simply ends against the flat cream. Never use black, grey, brown "
    "or any dark outline anywhere in the image."
)

WIDE = "16:9"

LAYERS = {
    "sky-far": dict(aspect=WIDE,
        prompt="A wide horizontal band of very distant small clouds, hazy and "
        "delicate, scattered thinly with generous empty space between them. "
        "Barely-there wisps, minimal detail, soft atmospheric haze."),
    "sky-mid": dict(aspect=WIDE,
        prompt="A horizontal drift of mid-distance fluffy clouds, rounded and "
        "billowing, softly lit from above with pale blush warmth pooling in "
        "their hollows. Arranged in a few separate clusters with wide open "
        "gaps between them."),
    "sky-near": dict(aspect=WIDE,
        prompt="Large, close, softly rounded cloud forms entering from the "
        "left and right edges of the frame, with the centre of the frame left "
        "completely open and empty. Plump billowing lobes with visible soft "
        "shading and gentle blush underlighting."),
    "sky-front": dict(aspect=WIDE,
        prompt="Two or three very large, very soft, out-of-focus cloud masses "
        "drifting across the frame as if passing directly in front of the "
        "viewer's face. Heavily blurred, translucent, feathered wispy edges."),
    "cloud-floor": dict(aspect=WIDE,
        prompt="A soft billowing floor of cloud tops seen from just above, "
        "like the calm surface of a sea of clouds, warm blush and cream light "
        "pooling across it. The cloud tops occupy the lower two thirds; above "
        "them is only flat empty background."),
    "island-base": dict(
        prompt="A single small floating cloud island seen from slightly "
        "above: a soft rounded cushion of cloud with a gently tapering wispy "
        "underside, as if something could rest on top of it. Centred, with "
        "plenty of empty space around it."),
    "island-misty": dict(
        prompt="A single floating cloud island that is half-formed and "
        "dissolving into mist, softer and vaguer and less resolved than a "
        "solid cloud, as if it is still being dreamed. Faint, translucent, "
        "with edges melting away into nothing."),
    "motes": dict(
        prompt="Scattered tiny soft glowing dust motes and gentle sparkles of "
        "light, widely spaced across an otherwise completely empty frame. "
        "Very subtle dreamy bokeh, pale mint and warm cream glows. Each mote is "
        "a soft luminous pale dot with no outline and no dark ring."),
}


def read_key():
    key = os.environ.get("OPENAI_API_KEY") or os.environ.get("OPENROUTER_API_KEY")
    if key:
        return key.strip()
    envfile = ROOT / ".env"
    if not envfile.exists():
        return None
    raw = envfile.read_bytes()
    for enc in ("utf-8-sig", "utf-16", "utf-8", "latin-1"):
        try:
            text = raw.decode(enc)
        except (UnicodeDecodeError, UnicodeError):
            continue
        for line in text.splitlines():
            line = line.strip().lstrip("﻿")
            if line.split("=")[0].strip() in ("OPENAI_API_KEY", "OPENROUTER_API_KEY"):
                val = line.partition("=")[2].strip().strip('"').strip("'")
                if val:
                    return val
    return None


def build_prompt(spec, plate="cream"):
    tail = PLATE_CREAM if plate == "cream" else PLATE
    return f"{STYLE}\n\n{spec['prompt']}\n\n{tail}"


def logo_data_uri():
    b = LOGO.read_bytes()
    return "data:image/png;base64," + base64.b64encode(b).decode()


def call(key, model, prompt, with_reference=True, aspect=None):
    content = [{"type": "text", "text": prompt}]
    if with_reference and LOGO.exists():
        content.append({"type": "image_url",
                        "image_url": {"url": logo_data_uri()}})
    body = {
        "model": model,
        "modalities": ["image", "text"],
        "messages": [{"role": "user", "content": content}],
    }
    if aspect:
        body["image_config"] = {"aspect_ratio": aspect}
    req = urllib.request.Request(
        API,
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}",
                 "Content-Type": "application/json",
                 "X-Title": "Midori Fuwafuwa art"},
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def extract_images(resp):
    out = []
    for choice in resp.get("choices", []):
        msg = choice.get("message", {}) or {}
        for im in (msg.get("images") or []):
            url = (im.get("image_url") or {}).get("url", "")
            if url.startswith("data:"):
                out.append(base64.b64decode(url.split(",", 1)[1]))
    return out


def matte(im, core_thresh=55, feather=1.6):
    """Two-zone matte for light art shot on a black plate.

    Neither naive approach works alone:

    * alpha = luminance is correct at the *edges* (a pixel that is 30% cloud
      reads at 30% brightness over black, so 30% alpha is exactly right) —
      but it wrongly makes the cloud's own dark sage/blush shading
      semi-transparent, and that shading is what gives the clouds form.
    * alpha = threshold keeps the shading solid, but bakes the black plate
      into every anti-aliased edge pixel, leaving a dark rim.

    So: find the painted body, hold it fully opaque, and use the
    luminance matte only in the thin boundary band outside it — where the
    colour is also unpremultiplied (divided by alpha) to strip the black
    the plate contributed. Result: solid shading, no dark fringe, soft edges.
    """
    import numpy as np
    from PIL import Image
    from scipy import ndimage

    rgb = np.asarray(im.convert("RGB")).astype(np.float32)
    lum = rgb.max(axis=2)  # max-channel: pale tints stay bright

    body = ndimage.binary_fill_holes(lum > core_thresh)
    body = ndimage.binary_erosion(body, iterations=1)
    body_soft = ndimage.gaussian_filter(body.astype(np.float32), feather)

    a = np.maximum(lum / 255.0, body_soft)
    a = np.clip(a, 0.0, 1.0)

    # unpremultiply: observed = true * a  →  true = observed / a
    safe = np.maximum(a, 1e-3)[..., None]
    out = np.clip(rgb / safe, 0, 255)
    out[a < 0.004] = 0

    arr = np.concatenate([out, (a * 255)[..., None]], axis=2).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def matte_cream(im, tol=14, feather=1.1):
    """Cut flat-cream-plate art by flooding in from the frame border.

    Crucially this is connected-component, not a global colour key: cream
    *inside* the artwork is never reached from the border, so pale cream
    highlights in the clouds survive — the same reason this worked on the
    logo, where the mascot's near-white body stayed intact.
    """
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter

    rgb = im.convert("RGB")
    w, h = rgb.size
    work = rgb.copy()
    SENT = (255, 0, 255)
    seeds = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
             (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)]
    for s in seeds:
        if work.getpixel(s) != SENT:
            ImageDraw.floodfill(work, s, SENT, thresh=tol)
    a = np.asarray(work)
    isbg = (a[:, :, 0] == 255) & (a[:, :, 1] == 0) & (a[:, :, 2] == 255)
    alpha = Image.fromarray(np.where(isbg, 0, 255).astype("uint8"))
    alpha = alpha.filter(ImageFilter.GaussianBlur(feather))
    out = rgb.convert("RGBA")
    out.putalpha(alpha)
    return out


def save(name, png_bytes, keep_raw=True, plate='cream'):
    from PIL import Image
    OUT.mkdir(parents=True, exist_ok=True)
    raw = Image.open(io.BytesIO(png_bytes))
    if keep_raw:
        raw.convert("RGB").save(OUT / f"{name}_raw.png", optimize=True)
    im = matte_cream(raw) if plate == 'cream' else matte(raw)
    im.save(OUT / f"{name}.png", optimize=True)
    im.save(OUT / f"{name}.webp", "WEBP", quality=90, method=6)
    kb = (OUT / f"{name}.webp").stat().st_size // 1024
    print(f"  saved {name}.png {im.size}  ({kb} KB webp)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", action="append")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--model", default="pro", choices=list(MODELS))
    ap.add_argument("--no-reference", action="store_true")
    ap.add_argument("--plate", default="cream", choices=["cream","black"])
    ap.add_argument("--rematte", action="store_true",
                    help="re-cut the matte from saved _raw plates; no API calls")
    ap.add_argument("--lo", type=int, default=3)
    ap.add_argument("--hi", type=int, default=34)
    args = ap.parse_args()

    names = args.only or list(LAYERS)
    bad = [n for n in names if n not in LAYERS]
    if bad:
        sys.exit(f"unknown layer(s): {', '.join(bad)}\nknown: {', '.join(LAYERS)}")

    if args.list:
        for n in names:
            print(n)
        return
    if args.dry_run:
        for n in names:
            print(f"\n===== {n} =====\n{build_prompt(LAYERS[n])}")
        return

    if args.rematte:
        from PIL import Image
        for n in names:
            raw = OUT / f"{n}_raw.png"
            if not raw.exists():
                print(f"  skip {n}: no saved plate")
                continue
            im = (matte_cream(Image.open(raw)) if args.plate == 'cream'
                  else matte(Image.open(raw), core_thresh=args.lo))
            im.save(OUT / f"{n}.png", optimize=True)
            im.save(OUT / f"{n}.webp", "WEBP", quality=90, method=6)
            print(f"  rematted {n} (lo={args.lo} hi={args.hi})")
        return

    key = read_key()
    if not key:
        sys.exit("No API key found (env OPENAI_API_KEY/OPENROUTER_API_KEY or .env).")

    model = MODELS[args.model]
    print(f"model: {model}")
    for n in names:
        print(f"\n>> {n}")
        try:
            resp = call(key, model, build_prompt(LAYERS[n], args.plate),
                        with_reference=not args.no_reference,
                        aspect=LAYERS[n].get("aspect"))
            imgs = extract_images(resp)
            if not imgs:
                txt = ""
                try:
                    txt = resp["choices"][0]["message"].get("content") or ""
                except Exception:
                    pass
                print(f"  no image returned. {str(txt)[:300]}")
                continue
            save(n, imgs[0], plate=args.plate)
        except urllib.error.HTTPError as e:
            print(f"  HTTP {e.code}: {e.read().decode()[:300]}")
        except Exception as e:
            print(f"  FAILED: {type(e).__name__}: {e}")

    print(f"\nDone. Art in {OUT}")


if __name__ == "__main__":
    main()
