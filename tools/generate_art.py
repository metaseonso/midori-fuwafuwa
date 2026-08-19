"""
Dreamland art generation.

Generates the layered parallax art for the studio site in the logo's own
painted style, using the official logo as a style reference image.

  Style source of truth: brand/logo/midori_fuwafuwa_logo_official.png
  Palette:               brand/DESIGN_SYSTEM.md  §1 (nothing outside it)

The key is read from the OPENAI_API_KEY environment variable and is never
written to disk, logged, or committed. The repo is public — do not put the
key in a file.

Usage
  python tools/generate_art.py --list             # show the layer plan
  python tools/generate_art.py --dry-run          # print prompts, no API calls
  python tools/generate_art.py --only sky-near    # generate one layer
  python tools/generate_art.py                    # generate everything

Output lands in site/public/images/dream/ as transparent PNG + WebP at
stable, unhashed filenames (guardrail 10: stable image URLs across deploys).
"""

import argparse
import base64
import io
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGO = ROOT / "brand" / "logo" / "midori_fuwafuwa_logo_official.png"
OUT = ROOT / "site" / "public" / "images" / "dream"

MODEL = "gpt-image-1"

# ---------------------------------------------------------------------------
# The house style. Prepended to every prompt so all layers read as one world.
# Written against DESIGN_SYSTEM §1 (palette) and §6 (illustration rules).
# ---------------------------------------------------------------------------
STYLE = (
    "Soft-painted kawaii storybook illustration in the exact style of the "
    "reference image: airbrushed pastel gouache with gentle blended shading, "
    "delicate thin soft edges, no hard black outlines, no bold vector strokes, "
    "no cel shading. Dreamy, weightless, fluffy (fuwa-fuwa). "
    "Strict palette: cream #F4EDD8, mint #BEECCE, soft mint #D1EFDE, "
    "pale mint highlight #EDF1EB, blush pink #F8D1D1, pale blush #FCF2F4, "
    "sage #748872, pale sage #DADBCE. "
    "Cream and very pale tints dominate; mint and blush appear only as soft "
    "accents. Low contrast, high key, luminous. No text, no letters, no logo, "
    "no characters, no faces."
)

TRANSPARENT = "Isolated on a fully transparent background."

LAYERS = {
    # ---- the descent: four depths of cloud -----------------------------
    "sky-far": dict(
        size="1536x1024",
        prompt=(
            "A wide band of very distant clouds, tiny and hazy, spread thinly "
            "across the frame with generous empty space between them. Barely "
            "there — the palest mint and cream, almost dissolving into air. "
            "Minimal detail, soft focus, atmospheric haze. " + TRANSPARENT
        ),
    ),
    "sky-mid": dict(
        size="1536x1024",
        prompt=(
            "A horizontal drift of mid-distance fluffy clouds, rounded and "
            "billowing, softly lit from above with pale blush warmth in their "
            "hollows. Moderate size, arranged with wide gaps between clusters, "
            "left and right thirds of the frame mostly open. " + TRANSPARENT
        ),
    ),
    "sky-near": dict(
        size="1536x1024",
        prompt=(
            "Large, close, softly rounded cloud forms entering from the left "
            "and right edges of the frame, with the centre left open and empty. "
            "Plump billowing lobes, visible soft shading, gentle blush "
            "underlighting. The nearest clouds in a dreamy sky. " + TRANSPARENT
        ),
    ),
    "sky-front": dict(
        size="1536x1024",
        prompt=(
            "Two or three very large, very soft, out-of-focus cloud masses "
            "drifting across the frame, as if passing directly in front of the "
            "viewer. Heavily blurred, translucent, wispy edges. Mostly empty "
            "space in the middle of the frame. " + TRANSPARENT
        ),
    ),
    # ---- ground the descent lands on ------------------------------------
    "cloud-floor": dict(
        size="1536x1024",
        prompt=(
            "A soft billowing floor of cloud tops seen from just above, like "
            "the surface of a sea of clouds, warm blush and cream light pooling "
            "across it, fading out at the top edge into nothing. " + TRANSPARENT
        ),
    ),
    # ---- islands the fields sit on --------------------------------------
    "island-base": dict(
        size="1024x1024",
        prompt=(
            "A single small floating cloud island seen from slightly above: a "
            "soft rounded cushion of cloud with a gently tapering wispy "
            "underside, as if it could hold something on top. Centred, plenty "
            "of empty space around it. Soft mint and cream with blush "
            "underlight. " + TRANSPARENT
        ),
    ),
    "island-misty": dict(
        size="1024x1024",
        prompt=(
            "A single floating cloud island that is half-formed and dissolving "
            "into mist — softer, vaguer and less resolved than a solid cloud, "
            "as if it is still being dreamed. Faint, translucent, edges melting "
            "away. Pale sage and cream. " + TRANSPARENT
        ),
    ),
    # ---- atmosphere -----------------------------------------------------
    "motes": dict(
        size="1024x1024",
        prompt=(
            "Scattered tiny soft glowing dust motes and gentle sparkles of "
            "light, widely spaced across an otherwise empty frame. Pale mint "
            "and warm cream glows, very subtle, dreamy bokeh. " + TRANSPARENT
        ),
    ),
}


def read_key():
    """Environment first, then a gitignored .env at the repo root.

    The key is returned, never printed or written anywhere.
    """
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        return key.strip()
    envfile = ROOT / ".env"
    if not envfile.exists():
        return None
    # PowerShell writes UTF-16LE with `>` and UTF-8-BOM with Set-Content,
    # so decode defensively rather than assuming plain UTF-8.
    raw = envfile.read_bytes()
    for enc in ("utf-8-sig", "utf-16", "utf-8", "latin-1"):
        try:
            text = raw.decode(enc)
        except (UnicodeDecodeError, UnicodeError):
            continue
        for line in text.splitlines():
            line = line.strip().lstrip('﻿')
            if line.startswith("OPENAI_API_KEY"):
                _, _, val = line.partition("=")
                val = val.strip().strip('"').strip("'")
                if val:
                    return val
    return None


def build_prompt(spec):
    return STYLE + " " + spec["prompt"]


def save(name, png_bytes):
    from PIL import Image

    OUT.mkdir(parents=True, exist_ok=True)
    im = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
    png = OUT / f"{name}.png"
    webp = OUT / f"{name}.webp"
    im.save(png, optimize=True)
    im.save(webp, "WEBP", quality=90, method=6)
    opaque = (im.getchannel("A").point(lambda a: 255 if a > 200 else 0)
              .convert("L").getextrema())
    print(f"  saved {png.name} {im.size}  "
          f"({png.stat().st_size // 1024} KB png / {webp.stat().st_size // 1024} KB webp)"
          f"{'  [WARNING: no transparency detected]' if opaque == (255, 255) else ''}")


def generate(client, name, spec, use_reference=True):
    prompt = build_prompt(spec)
    print(f"\n>> {name}  ({spec['size']})")
    if use_reference and LOGO.exists():
        with open(LOGO, "rb") as ref:
            result = client.images.edit(
                model=MODEL,
                image=[ref],
                prompt=prompt,
                size=spec["size"],
                background="transparent",
            )
    else:
        result = client.images.generate(
            model=MODEL,
            prompt=prompt,
            size=spec["size"],
            background="transparent",
        )
    save(name, base64.b64decode(result.data[0].b64_json))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", action="append", help="generate only this layer (repeatable)")
    ap.add_argument("--dry-run", action="store_true", help="print prompts, make no API calls")
    ap.add_argument("--list", action="store_true", help="list the layer plan and exit")
    ap.add_argument("--no-reference", action="store_true",
                    help="do not send the logo as a style reference")
    args = ap.parse_args()

    names = args.only or list(LAYERS)
    unknown = [n for n in names if n not in LAYERS]
    if unknown:
        sys.exit(f"unknown layer(s): {', '.join(unknown)}\nknown: {', '.join(LAYERS)}")

    if args.list:
        for n in names:
            print(f"{n:14s} {LAYERS[n]['size']}")
        return

    if args.dry_run:
        for n in names:
            print(f"\n===== {n} ({LAYERS[n]['size']}) =====\n{build_prompt(LAYERS[n])}")
        return

    key = read_key()
    if not key:
        sys.exit(
            "No API key found.\n\n"
            "Put it in a .env file at the repo root (git ignores this file —\n"
            "verified against .gitignore, it cannot be committed):\n\n"
            "  OPENAI_API_KEY=sk-...\n\n"
            "or set it in the environment of the shell you run this from."
        )

    try:
        from openai import OpenAI
    except ImportError:
        sys.exit("pip install openai pillow")

    client = OpenAI(api_key=key)
    for n in names:
        try:
            generate(client, n, LAYERS[n], use_reference=not args.no_reference)
        except Exception as e:
            print(f"  FAILED {n}: {type(e).__name__}: {e}")

    print(f"\nDone. Art in {OUT}")


if __name__ == "__main__":
    main()
