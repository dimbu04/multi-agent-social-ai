import asyncio
asyncio.set_event_loop_policy(
    asyncio.WindowsProactorEventLoopPolicy()
)

from playwright.sync_api import sync_playwright
import sys


def post_to_linkedin(content):

    try:

        with sync_playwright() as p:

            browser = p.chromium.connect_over_cdp(
                "http://localhost:9222"
            )

            context = browser.contexts[0]

            page = None

            for pg in context.pages:
                if "linkedin.com" in pg.url:
                    page = pg
                    break


            if not page:
                return False,"Open LinkedIn first"


            # IMPORTANT:
            # LinkedIn needs active foreground tab
            page.bring_to_front()

            page.wait_for_timeout(1500)


            print("Opening post composer...")


            # safer fallback selectors
            try:

                page.locator(
                    'button:has-text("Start a post")'
                ).first.click(
                    timeout=8000
                )

            except:

                try:
                    page.get_by_text(
                        "Start a post"
                    ).first.click(
                        timeout=8000
                    )

                except:
                    page.locator(
                        "[data-test-modal-trigger]"
                    ).first.click(
                        timeout=8000
                    )


            page.wait_for_timeout(1500)


            print("Pasting content...")


            box = page.locator(
                "[role='textbox']"
            ).last

            box.click()


            # FAST paste
            page.keyboard.insert_text(
                content[:2500]
            )


            page.wait_for_timeout(1000)


            print("Publishing...")


            try:
                page.locator(
                  "div[role='dialog'] button.artdeco-button--primary"
                ).click()

            except:
                page.locator(
                  "button:has-text('Post')"
                ).first.click()


            page.wait_for_timeout(3000)

            return True,"LinkedIn Posted Successfully"



    except Exception as e:
        return False,str(e)



if __name__=="__main__":

    content=(
      sys.argv[1]
      if len(sys.argv)>1
      else "LinkedIn automation test"
    )

    print(
       post_to_linkedin(content)
    )