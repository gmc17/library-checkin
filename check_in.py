#!/usr/bin/env python3
"""
Decides which code to submit, based on the current UTC hour.
(adjust if you prefer local 'America/Chicago' logic)
"""
import datetime
import sys
from playwright.sync_api import sync_playwright

def do_check_in(res_code):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://rooms.lib.uchicago.edu/r/checkin")

        page.fill("#s-lc-code", res_code)
        page.click("#s-lc-checkin-button")

        page.wait_for_selector("#s-lc-success-message", state="visible", timeout=10000)
        success_text = page.inner_text("#s-lc-success-message")
        print(f"Check-in for code={res_code} succeeded: {success_text}")

        browser.close()

def main():
    """Check the current UTC hour, decide which code to run."""
    now_utc = datetime.datetime.utcnow()
    hour_utc = now_utc.hour

    # Example schedule (UTC):
    # 15:00 UTC -> 2SD
    # 18:00 UTC -> 59M
    # 21:00 UTC -> 6XT
    #  0:00 UTC -> F2P
    #  3:00 UTC -> ??? (maybe another code)

    code_for_hour = {
        15: "2SD",  # 9am CST
        18: "59M",  # 12pm CST
        21: "6XT",  # 3pm CST
         0: "F2P",  # 6pm CST
         3: "ABC",  # 9pm CST (example)
    }

    if hour_utc in code_for_hour:
        chosen_code = code_for_hour[hour_utc]
        do_check_in(chosen_code)
    else:
        print(f"No code mapped for hour {hour_utc} UTC; skipping.")

if __name__ == "__main__":
    main()
