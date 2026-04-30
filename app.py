import streamlit as st
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
import warnings
warnings.filterwarnings("ignore")

from main import run_pipeline, chat_refine


# ---------------- PAGE ----------------

st.set_page_config(
    page_title="AI Social Media Generator",
    layout="wide"
)

st.title("🚀 Multi-Agent Social Media Generator")
st.caption(
"Generate • Refine • Publish • Auto Post"
)


# ---------- DASHBOARD ----------

c1,c2,c3,c4,c5 = st.columns(5)

c1.metric("Platforms","3")
c2.metric("Agents","5")
c3.metric("Auto Posting","Enabled")
c4.metric("Execution","Parallel")
c5.metric("Posts Automated","3")


# ---------------- SESSION ----------------

defaults={
"result":None,
"current_content":"",
"final_content":None
}

for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k]=v



# ------------ SUBPROCESS RUNNER ------------

def run_post(script,content):

    try:

        r=subprocess.run(
            [sys.executable,script,content],
            capture_output=True,
            text=True
        )

        out=r.stdout.strip()
        err=r.stderr.strip()

        if r.returncode==0 and "False" not in out:
            return True,out

        return False,out or err

    except Exception as e:
        return False,str(e)



# ---------------- GENERATE ----------------

st.divider()

url=st.text_input(
"🔗 Enter Blog URL"
)

platform=st.selectbox(
"Choose Platform",
["All","LinkedIn","Twitter","Instagram"]
)


if st.button("✨ Generate Content"):

    if not url:
        st.warning("Enter URL")

    else:

        progress=st.progress(0)
        agent_log=st.empty()

        agent_log.info(
        "🔎 Scraper Agent Running..."
        )
        progress.progress(20)

        time.sleep(.6)

        agent_log.info(
        "✍ Content Agents Generating..."
        )

        result=run_pipeline(
            url,
            platform
        )

        progress.progress(75)

        time.sleep(.6)

        agent_log.success(
        "✅ Content Generation Complete"
        )

        progress.progress(100)

        st.session_state.result=result



linkedin_content=""
twitter_content=""
instagram_content=""
combined=""



# ---------------- SHOW CONTENT ----------------

if st.session_state.result:

    result=st.session_state.result

    st.success(
      "Generated Successfully"
    )


    if platform=="All":

        t1,t2,t3=st.tabs(
         ["LinkedIn","Twitter","Instagram"]
        )

        linkedin_content=result["linkedin"]
        twitter_content=result["twitter"]
        instagram_content=result["instagram"]


        with t1:
            st.text_area(
              "LinkedIn Content",
              linkedin_content,
              height=260
            )

        with t2:
            st.text_area(
              "Twitter Content",
              twitter_content,
              height=260
            )

        with t3:
            st.text_area(
              "Instagram Content",
              instagram_content,
              height=260
            )


        combined=f"""
{linkedin_content}


{twitter_content}


{instagram_content}
"""

    else:

        single=result[
            platform.lower()
        ]

        linkedin_content=single
        twitter_content=single
        instagram_content=single

        combined=single

        st.text_area(
            "Generated Content",
            single,
            height=300
        )



# ------------ REFINE ------------

st.divider()

st.subheader(
"💬 AI Content Assistant"
)

if combined:

    st.text_area(
      "Current Content",
      combined,
      height=250
    )


edit=st.text_input(
"Modify Content"
)

if st.button("Send") and edit:

    updated=chat_refine(
      combined,
      edit,
      []
    )

    st.write(updated)


if st.button(
"🚀 Finalize Content"
):
    st.success(
      "Content Finalized"
    )



# -------- Agent Activity --------

st.divider()

st.subheader(
"🤖 Agent Activity"
)

st.info("""
Scraper Agent Ready  
Content Agents Ready  
Publisher Agents Ready
""")


# ------------ PUBLISH CENTER ------------

st.divider()

st.subheader(
"📢 Publishing Center"
)

a,b,c,d=st.columns(4)



# -------- INDIVIDUAL --------

with a:

    if st.button("💼 LinkedIn"):

        ok,msg=run_post(
          "post_linkedin_playwright.py",
          linkedin_content
        )

        if ok:
            st.success(msg)
        else:
            st.error(msg)



with b:

    if st.button("🐦 Twitter"):

        ok,msg=run_post(
         "post_twitter_playwright.py",
         twitter_content
        )

        if ok:
            st.success(msg)
        else:
            st.error(msg)



with c:

    if st.button("📸 Instagram"):

        ok,msg=run_post(
          "post_instagram_playwright.py",
          instagram_content
        )

        if ok:
            st.success(msg)
        else:
            st.error(msg)




# ---------- PARALLEL JOBS ----------

def linkedin_job(content):
    return run_post(
       "post_linkedin_playwright.py",
       content
    )


def twitter_job(content):
    return run_post(
       "post_twitter_playwright.py",
       content
    )


def instagram_job(content):
    return run_post(
      "post_instagram_playwright.py",
      content
    )




# ---------- MULTI AGENT PUBLISH ----------

with d:

    if st.button(
      "🚀 Launch Multi-Agent Publishing"
    ):

        if not st.session_state.result:
            st.warning(
              "Generate content first"
            )
            st.stop()


        bar=st.progress(0)

        launch_status=st.empty()

        linkedin_status=st.empty()
        twitter_status=st.empty()
        insta_status=st.empty()


        launch_status.info(
          "🚀 Launching Publisher Agents..."
        )

        bar.progress(10)

        linkedin_status.warning(
         "🟡 LinkedIn Posting..."
        )

        twitter_status.info(
         "⏳ Twitter Waiting..."
        )

        insta_status.info(
         "⏳ Instagram Waiting..."
        )


        with ThreadPoolExecutor(
            max_workers=3
        ) as ex:

            f1=ex.submit(
                linkedin_job,
                result["linkedin"]
            )

            f2=ex.submit(
                twitter_job,
                result["twitter"]
            )

            f3=ex.submit(
                instagram_job,
                result["instagram"]
            )


            # LinkedIn
            li=f1.result()

            bar.progress(35)

            if li[0]:
                linkedin_status.success(
                 "🟢 LinkedIn Done"
                )
            else:
                linkedin_status.error(
                 "🔴 LinkedIn Failed"
                )


            # Twitter starts
            twitter_status.warning(
              "🟡 Twitter Posting..."
            )

            tw=f2.result()

            bar.progress(65)

            if tw[0]:
                twitter_status.success(
                 "🟢 Twitter Done"
                )
            else:
                twitter_status.error(
                 "🔴 Twitter Failed"
                )


            # Insta starts
            insta_status.warning(
              "🟡 Instagram Posting..."
            )

            ig=f3.result()

            bar.progress(90)

            if ig[0]:
                insta_status.success(
                  "🟢 Instagram Done"
                )
            else:
                insta_status.error(
                  "🔴 Instagram Failed"
                )


        bar.progress(100)

        launch_status.success(
         "✅ Publisher Agents Completed"
        )


        st.write("## Results")


        if li[0]:
            st.success(
             "LinkedIn Posted"
            )
        else:
            st.error(li[1])


        if tw[0]:
            st.success(
             "Twitter Posted"
            )
        else:
            st.error(tw[1])


        if ig[0]:
            st.success(
             "Instagram Posted"
            )
        else:
            st.error(ig[1])


        if li[0] and tw[0] and ig[0]:

            st.balloons()

            st.success(
             "🎉 Posted To All Platforms"
            )



# ------------ DOWNLOADS ------------

st.divider()

if combined:

    st.download_button(
      "Download TXT",
      combined,
      "content.txt"
    )


if st.session_state.result:

    st.download_button(
      "Download JSON",
      json.dumps(
        st.session_state.result,
        indent=2
      ),
      "content.json"
    )