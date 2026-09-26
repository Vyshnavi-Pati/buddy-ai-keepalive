import sys

from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError,
)


BUDDY_URL = "https://buddy-ai-bw79mv532plmnhuqewq2mh.streamlit.app"


def wake_buddy() -> bool:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        try:
            page = browser.new_page()

            print("Opening Buddy AI...")

            page.goto(
                BUDDY_URL,
                wait_until="domcontentloaded",
                timeout=60000,
            )

            print(f"Loaded: {page.url}")

            wake_button = page.get_by_role(
                "button",
                name="Yes, get this app back up!",
            )

            try:
                wake_button.wait_for(
                    state="visible",
                    timeout=10000,
                )

                print("Buddy AI is sleeping!")
                print("Waking it up...")

                wake_button.click()

                print("Wake up button clicked!")
                print("Buddy AI is waking up.")

            except PlaywrightTimeoutError:
                print("Buddy AI is already awake.")

            return True

        except Exception as e:
            print(f"Automation failed: {e}")
            return False

        finally:
            browser.close()


success = wake_buddy()

if not success:
    sys.exit(1)