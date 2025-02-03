#!/usr/bin/env python3

import sys
from playwright.sync_api import sync_playwright

def do_check_in(check_in_code):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Replace with your real check-in URL
        page.goto("https://rooms.lib.uchicago.edu/r/checkin")

        # Fill the check-in code (no success waiting)
        page.fill("#s-lc-code", check_in_code)

        # Click "Check In"
        page.click("#s-lc-checkin-button")

        # Optional short pause so the click has time to fire
        # Remove or adjust if you truly want zero waiting.
        page.wait_for_timeout(2000)

        browser.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        code = sys.argv[1]
    else:
        code = "DEFAULT_CODE"

    do_check_in(code)
