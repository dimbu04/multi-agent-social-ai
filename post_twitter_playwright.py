import asyncio
asyncio.set_event_loop_policy(
 asyncio.WindowsProactorEventLoopPolicy()
)

from playwright.sync_api import sync_playwright
import sys


def post_to_twitter(content):

    try:

        content=content[:240]

        with sync_playwright() as p:

            browser=p.chromium.connect_over_cdp(
               "http://localhost:9223"
            )

            context=browser.contexts[0]

            page=None

            for pg in context.pages:
                if "x.com" in pg.url:
                    page=pg
                    break

            if not page:
                return False,"Open X first"


            page.bring_to_front()

            page.goto(
              "https://x.com/compose/post"
            )

            page.wait_for_timeout(4000)


            print("Finding tweet box...")


            box=page.locator(
              '[data-testid="tweetTextarea_0"]'
            ).first


            box.fill(
               content
            )


            page.wait_for_timeout(1500)


            print("Posting tweet...")


            # KEYBOARD POST
            page.keyboard.press(
                "Control+Enter"
            )


            page.wait_for_timeout(5000)

            return True,"Twitter Posted Successfully"


    except Exception as e:
        return False,str(e)



if __name__=="__main__":

    content=(
      sys.argv[1]
      if len(sys.argv)>1
      else "Twitter automation test"
    )

    print(
       post_to_twitter(content)
    )