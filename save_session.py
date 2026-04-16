from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Open LinkedIn login page
    page.goto("https://www.linkedin.com/login")

    # You will login manually in the opened browser
    input("➡️ Login manually in the browser, then press ENTER here...")

    # Save cookies/session
    context.storage_state(path="state.json")

    print("✅ Session saved as state.json")

    browser.close()