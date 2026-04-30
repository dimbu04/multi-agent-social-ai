import asyncio
asyncio.set_event_loop_policy(
 asyncio.WindowsProactorEventLoopPolicy()
)
from generate_image import create_post_image


from playwright.sync_api import sync_playwright
import time
import sys


def post_to_instagram(content):
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(
                "http://localhost:9224"
            )

            context = browser.contexts[0]

            page = None

            for pg in context.pages:
                if "instagram.com" in pg.url:
                    page = pg
                    break

            # page.bring_to_front()

            print("Opening Instagram...")

            page.goto(
                "https://instagram.com",
                wait_until="domcontentloaded",
                timeout=60000
            )

            time.sleep(2)

            print("Create menu...")
            page.locator(
                "svg[aria-label='New post']"
            ).click()

            time.sleep(3)

            print("Click Post...")
            page.get_by_role(
                "link",
                name="Post Post"
            ).click()

            time.sleep(4)

            print("Upload image...")
            page.locator(
                "input[type='file']"
            ).set_input_files(
                r"C:\Users\manup\multi-agent-social-ai\post_image.jpg"
            )

            time.sleep(5)

            print("Next 1")
            page.get_by_text(
                "Next"
            ).click()

            time.sleep(4)

            print("Next 2")
            page.get_by_text(
                "Next"
            ).click()

            time.sleep(4)

            print("Typing caption...")

            box = page.locator(
                "div[contenteditable='true']"
            ).last

            box.click()

            box.fill(
                content[:2000]
            )

            time.sleep(3)

            print("Share post...")

            page.get_by_role(
                "button",
                name="Share"
            ).click()

            time.sleep(10)

            return True,"Instagram posted"

    except Exception as e:
        return False, str(e)


# ---- for Post All ----

if __name__ == "__main__":
    content = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "Demo Instagram Caption"
    )

    create_post_image(
 content
)

    success, msg = post_to_instagram(
        content
    )

    print(msg)