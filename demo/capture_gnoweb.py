#!/usr/bin/env python3
"""Headless Playwright captures of live gnoweb pages."""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path("/workspace/bounties/hearthescrow/demo/shots")
OUT.mkdir(parents=True, exist_ok=True)
PAGES = [
    ("dashboard", "https://onyx.testnets.gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow", "HearthEscrow"),
    ("escrow1", "https://onyx.testnets.gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow:escrow/1", "Smoke Release"),
    ("escrow2", "https://onyx.testnets.gno.land/r/g1x7ud67jym95qh9zf0swmq6ck07s3ly3lksxc5n/hearthescrow:escrow/2", "Smoke Refund"),
]

def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        page = browser.new_page(viewport={"width": 1280, "height": 800}, device_scale_factor=1)
        for name, url, needle in PAGES:
            page.goto(url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(1500)
            body = page.inner_text("body")
            if needle not in body:
                raise SystemExit(f"{name}: missing {needle!r} at {url}")
            dest = OUT / f"{name}.png"
            page.screenshot(path=str(dest), full_page=False)
            print("wrote", dest, "ok", needle)
        browser.close()

if __name__ == "__main__":
    main()
