import streamlit as st
import json
from main import run_pipeline, chat_refine
from post_linkedin_playwright import post_to_linkedin

st.set_page_config(page_title="AI Social Media Generator", layout="wide")

# ---------------- TITLE ----------------
st.markdown("<h1 style='text-align: center;'>🚀 Multi-Agent Social Media Content Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Generate LinkedIn, Twitter, Instagram & Reel content from any URL</p>", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "result" not in st.session_state:
    st.session_state.result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_content" not in st.session_state:
    st.session_state.current_content = ""

if "final_content" not in st.session_state:
    st.session_state.final_content = None

# ---------------- INPUT ----------------
url = st.text_input("🔗 Enter Blog URL")

platform = st.selectbox(
    "📱 Select Platform",
    ["All", "LinkedIn", "Twitter", "Instagram", "Reel"]
)

# ---------------- GENERATE ----------------
if st.button("✨ Generate Content"):
    if not url:
        st.warning("⚠️ Please enter a URL")
    else:
        with st.spinner("🤖 AI Agents are working..."):
            st.session_state.result = run_pipeline(url)
            st.session_state.chat_history = []
            st.session_state.current_content = ""
            st.session_state.final_content = None

# ---------------- SHOW OUTPUT ----------------
if st.session_state.result:

    result = st.session_state.result

    st.success("✅ Content Generated Successfully!")

    with st.expander("📌 Summary"):
        st.write(result.get("summary", ""))

    with st.expander("🎯 Strategy"):
        st.write(result.get("strategy", ""))

    with st.expander("🏷️ Hashtags"):
        st.write(result.get("hashtags", ""))

    st.divider()

    # ---------------- CONTENT ----------------
    if platform == "All":
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("💼 LinkedIn")
            st.text_area("linkedin_output", result.get("linkedin", ""), height=250)

            st.subheader("🐦 Twitter")
            st.text_area("twitter_output", result.get("twitter", ""), height=250)

        with col2:
            st.subheader("📸 Instagram")
            st.text_area("instagram_output", result.get("instagram", ""), height=250)

            st.subheader("🎬 Reel Script")
            st.text_area("reel_output", result.get("reel", ""), height=250)

        selected_content = f"""
LINKEDIN:
{result.get("linkedin")}

TWITTER:
{result.get("twitter")}

INSTAGRAM:
{result.get("instagram")}

REEL:
{result.get("reel")}
"""
    else:
        selected_content = result.get(platform.lower(), "")
        st.subheader(f"📄 {platform} Content")
        st.text_area("single_output", selected_content, height=300)

    if st.session_state.current_content == "":
        st.session_state.current_content = selected_content

    # ---------------- CHAT ----------------
    st.divider()
    st.subheader("💬 AI Content Assistant")

    st.text_area("📝 Current Content", st.session_state.current_content, height=250)

    user_input = st.text_input("💬 Modify content", key="chat_input")

    if st.button("Send"):
        if user_input:
            updated = chat_refine(
                st.session_state.current_content,
                user_input,
                st.session_state.chat_history
            )

            st.session_state.chat_history.append(("User", user_input))
            st.session_state.chat_history.append(("AI", updated))
            st.session_state.current_content = updated

    st.subheader("🗨 Conversation")
    for role, msg in st.session_state.chat_history:
        if role == "User":
            st.write(f"🧑 You: {msg}")
        else:
            st.write(f"🤖 AI: {msg}")

    # ---------------- FINALIZE ----------------
    st.divider()
    st.subheader("✅ Final Approval")

    if st.button("🚀 Finalize Content"):
        st.session_state.final_content = st.session_state.current_content
        st.success("Content Finalized!")

    if st.session_state.final_content:
        st.text_area("📌 Final Content", st.session_state.final_content, height=300)

    # ---------------- POSTING ----------------
    st.divider()
    st.subheader("🚀 Post to Social Media")

    
    twitter_token = st.text_input("Twitter Token", type="password")
    insta_token = st.text_input("Instagram Token", type="password")
    ig_user = st.text_input("Instagram User ID")
    image_url = st.text_input("Image URL")

    col1, col2, col3 = st.columns(3)

    # LinkedIn
    with col1:
        if st.button("Post LinkedIn"):
            if not st.session_state.final_content:
                st.warning("Finalize content first")
            else:
                with st.spinner("Posting to LinkedIn..."):
                    post_to_linkedin(st.session_state.final_content)

                st.success("✅ Posted to LinkedIn successfully!")

    # Twitter
    with col2:
        if st.button("Post Twitter"):
            if not st.session_state.final_content:
                st.warning("Finalize first")
            elif not twitter_token:
                st.warning("Enter token")
            else:
                res = post_to_twitter(
                    st.session_state.final_content,
                    twitter_token
                )
                st.success("Posted to Twitter")
                st.write(res)

    # Instagram
    with col3:
        if st.button("Post Instagram"):
            if not st.session_state.final_content:
                st.warning("Finalize first")
            elif not insta_token or not ig_user or not image_url:
                st.warning("Enter all details")
            else:
                res = post_to_instagram(
                    st.session_state.final_content,
                    insta_token,
                    ig_user,
                    image_url
                )
                st.success("Posted to Instagram")
                st.write(res)

    # ---------------- DOWNLOAD ----------------
    output_text = f"""
SUMMARY:
{result.get("summary")}

STRATEGY:
{result.get("strategy")}

HASHTAGS:
{result.get("hashtags")}

LINKEDIN:
{result.get("linkedin")}
"""

    st.divider()
    st.subheader("⬇️ Download Results")

    st.download_button("Download TXT", output_text, "content.txt")
    st.download_button("Download JSON", json.dumps(result), "content.json")