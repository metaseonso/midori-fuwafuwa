"""Screenshot the deployed site, to confirm production matches local."""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://metaseonso.github.io/midori-fuwafuwa/"
SHOTS = Path(__file__).resolve().parent.parent / ".shots"

path = sys.argv[1] if len(sys.argv) > 1 else ""
scroll = int(sys.argv[2]) if len(sys.argv) > 2 else 0
out = sys.argv[3] if len(sys.argv) > 3 else "live.png"

SHOTS.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_context(viewport={"width": 1440, "height": 900},
                       device_scale_factor=2).new_page()
    pg.goto(BASE + path, wait_until="networkidle")
    pg.wait_for_timeout(1200)
    if scroll:
        pg.evaluate(f"window.scrollTo(0,{scroll})")
        pg.wait_for_timeout(800)
    pg.screenshot(path=str(SHOTS / out))
    print("wrote", out, "| page height", pg.evaluate("document.body.scrollHeight"))
    b.close()
