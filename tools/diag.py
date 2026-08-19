from playwright.sync_api import sync_playwright

JS = """() => {
  function box(sel){
    const e = document.querySelector(sel);
    if (!e) return sel + ' MISSING';
    const r = e.getBoundingClientRect();
    return sel + '  y=' + Math.round(r.y) + '..' + Math.round(r.bottom) +
           '  ' + Math.round(r.width) + 'x' + Math.round(r.height);
  }
  return [
    'viewport h=' + window.innerHeight,
    box('.arrival'),
    box('.arrival__stack'),
    box('.arrival__wordmark'),
    box('.arrival__mascot'),
    box('.arrival__studio'),
    box('.hint'),
  ].join('\\n');
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_context(viewport={"width": 1440, "height": 900}).new_page()
    pg.goto("http://localhost:4321/midori-fuwafuwa/", wait_until="networkidle")
    pg.wait_for_timeout(700)
    print(pg.evaluate(JS))
    b.close()
