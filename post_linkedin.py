from playwright.sync_api import sync_playwright


def post_to_linkedin(content):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=80)
        context = browser.new_context(storage_state="state.json")
        page = context.new_page()

        page.goto("https://www.linkedin.com/feed/")
        page.wait_for_timeout(5000)

        print("✅ Already logged in")

        # Open post box
        page.get_by_role("button", name="Start a post").first.click()
        page.wait_for_timeout(2000)
        print("✅ Post box opened")

        # Wait for editor
        editor = page.locator("div[contenteditable='true']").first
        editor.wait_for(state="visible", timeout=20000)

        # Type content slowly
        editor.click()
        page.keyboard.type(content, delay=40)
        page.wait_for_timeout(2000)

        print("✅ Content typed")

        # 🔥 IMPORTANT: find Post button INSIDE composer dialog only
        post_btn = page.get_by_role("button", name="Post").last

        # Wait until button becomes visible + enabled
        post_btn.wait_for(state="visible", timeout=20000)

        # small wait (LinkedIn enables button after typing)
        page.wait_for_timeout(2000)

        # Try clicking
        try:
            post_btn.click()
        except:
            # fallback force click
            post_btn.click(force=True)

        print("🚀 Post clicked")

        page.wait_for_timeout(5000)
        print("✅ Done")

        browser.close()


if __name__ == "__main__":
    post_to_linkedin("🚀 FINAL WORKING LINKEDIN POST FROM AI PROJECT 🔥")