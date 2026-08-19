"""Screenshot the site so design work can be judged by looking at it.

  python tools/shot.py                      # hero at desktop
  python tools/shot.py --scroll 1200        # after scrolling
  python tools/shot.py --full               # whole page, stitched
  python tools/shot.py --mobile
  python tools/shot.py --path fields/the-kits/
  python tools/shot.py --reduced            # prefers-reduced-motion
"""
import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SHOTS = ROOT / ".shots"
BASE = "http://localhost:4321/midori-fuwafuwa/"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default="")
    ap.add_argument("--scroll", type=int, default=0)
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--mobile", action="store_true")
    ap.add_argument("--reduced", action="store_true")
    ap.add_argument("--out", default=None)
    ap.add_argument("--wide", action="store_true")
    args = ap.parse_args()

    SHOTS.mkdir(exist_ok=True)
    w, h = (390, 844) if args.mobile else (1440, 900)
    if args.wide:
        w, h = 1920, 1080

    name = args.out or (
        f"{'mobile' if args.mobile else 'desktop'}"
        f"{'-reduced' if args.reduced else ''}"
        f"{'-full' if args.full else ''}"
        f"{('-s' + str(args.scroll)) if args.scroll else ''}.png"
    )

    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(
            viewport={"width": w, "height": h},
            device_scale_factor=2,
            reduced_motion="reduce" if args.reduced else "no-preference",
        )
        page = ctx.new_page()
        page.goto(BASE + args.path, wait_until="networkidle")
        page.wait_for_timeout(900)
        if args.scroll:
            page.evaluate(f"window.scrollTo(0,{args.scroll})")
            page.wait_for_timeout(700)
        page.screenshot(path=str(SHOTS / name), full_page=args.full)
        print("wrote", SHOTS / name)
        print("page height:", page.evaluate("document.body.scrollHeight"))
        b.close()


if __name__ == "__main__":
    main()
