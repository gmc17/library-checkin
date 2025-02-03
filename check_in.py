#!/usr/bin/env python3

import sys
from playwright.sync_api import sync_playwright

def do_check_in(check_in_code):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
      
        page.goto("https://rooms.lib.uchicago.edu/r/checkin")

        # Fill in the check-in code (the input with id="s-lc-code")
        page.fill("#s-lc-code", check_in_code)

        # Click the "Check In" button (id="s-lc-checkin-button")
        page.click("#s-lc-checkin-button")

        # Wait for the success message to appear
        #    (id="s-lc-success-message" is initially display:none, 
        #     so we wait for it to become visible or exist in the DOM)
        page.wait_for_selector("#s-lc-success-message", state="visible", timeout=10000)

        # Print out the success message text (for logging)
        success_text = page.inner_text("#s-lc-success-message")
        print("Success message says:", success_text)

        browser.close()

if __name__ == "__main__":
    # If you call the script like: python check_in.py ABC123
    if len(sys.argv) > 1:
        code = sys.argv[1]
    else:
        code = "DEFAULT_CODE"

    do_check_in(code)
