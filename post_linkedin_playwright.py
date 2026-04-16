import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from playwright.sync_api import sync_playwright


def post_to_linkedin(content):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=80)
        context = browser.new_context(storage_state="state.json")
        page = context.new_page()

        page.goto("https://www.linkedin.com/feed/")
        page.wait_for_timeout(5000)

        # Open post box
        page.get_by_role("button", name="Start a post").first.click()
        page.wait_for_timeout(2000)

        # Type content
        editor = page.locator("div[contenteditable='true']").first
        editor.wait_for(state="visible", timeout=20000)

        editor.click()
        page.keyboard.type(content, delay=40)
        page.wait_for_timeout(2000)

        # Click Post (inside dialog only)
        post_btn = page.get_by_role("button", name="Post").last

        post_btn.wait_for(state="visible", timeout=20000)
        page.wait_for_timeout(2000)

        try:
            post_btn.click()
        except:
            post_btn.click(force=True)

        page.wait_for_timeout(5000)
        browser.close()