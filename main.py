import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()


# ✅ LangChain Groq LLM
from langchain_groq import ChatGroq

llm = ChatGroq(
     model="llama-3.1-8b-instant", 
    groq_api_key=os.getenv("OPENAI_API_KEY")
)
# ✅ Embeddings (LangChain)
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

# 🌐 Scraper
import requests
import certifi
from bs4 import BeautifulSoup

def scraper_agent(state):
    url = state["url"]

    response = requests.get(url, verify=certifi.where())
    soup = BeautifulSoup(response.text, "html.parser")

    paragraphs = [p.text for p in soup.find_all("p")]
    content = " ".join(paragraphs[:50])

    return {"scraped_content": content}


# 🧠 Summarizer
def summarize_agent(state):
    content = state["scraped_content"]

    prompt = f"""
    Summarize the content and extract:
    - summary
    - key points
    - audience
    - tone

    Content:
    {content}
    """

    response = llm.invoke(prompt)

    return {"summary": response.content}


# 🎯 Planner
def planner_agent(state):
    summary = state["summary"]

    prompt = f"""
    Create social media strategy:
    - hook
    - tone
    - angle

    {summary}
    """

    response = llm.invoke(prompt)

    return {"strategy": response.content}


# 📱 Content Agents
def linkedin_agent(state):
    response = llm.invoke(f"Write LinkedIn post:\n{state['strategy']}")
    return {"linkedin": response.content}


def twitter_agent(state):
    response = llm.invoke(f"Write Twitter thread:\n{state['strategy']}")
    return {"twitter": response.content}


def instagram_agent(state):
    response = llm.invoke(f"Write Instagram caption + hashtags:\n{state['strategy']}")
    return {"instagram": response.content}


def reel_agent(state):
    response = llm.invoke(f"Write reel script:\n{state['summary']}")
    return {"reel": response.content}

def hashtag_agent(state):
    summary = state["summary"]

    prompt = f"""
    Generate trending and relevant social media hashtags.

    Requirements:
    - Mix of general + niche hashtags
    - Max 15 hashtags
    - Output as a single line (space-separated)
    - Keep them relevant to this content

    Content:
    {summary}
    """

    response = llm.invoke(prompt)

    return {"hashtags": response.content}


# 🔁 LangGraph Workflow
from langgraph.graph import StateGraph

from typing import TypedDict

class GraphState(TypedDict ):
    url: str
    scraped_content: str
    summary: str
    strategy: str
    linkedin: str
    twitter: str
    instagram: str
    reel: str
    hashtags: str

workflow = StateGraph(GraphState)

workflow.add_node("scraper", scraper_agent)
workflow.add_node("summarizer", summarize_agent)
workflow.add_node("planner", planner_agent)


workflow.add_node("linkedin", linkedin_agent)
workflow.add_node("twitter", twitter_agent)
workflow.add_node("instagram", instagram_agent)
workflow.add_node("reel", reel_agent)
workflow.add_node("hashtags", hashtag_agent)


workflow.set_entry_point("scraper")

workflow.add_edge("scraper", "summarizer")
workflow.add_edge("summarizer", "planner")

# parallel execution
workflow.add_edge("planner", "linkedin")
workflow.add_edge("planner", "twitter")
workflow.add_edge("planner", "instagram")
workflow.add_edge("summarizer", "reel")   # ✅ ADD
workflow.add_edge("planner", "hashtags")

workflow.set_finish_point("linkedin")

app = workflow.compile()

def run_pipeline(url: str):
    return app.invoke({"url": url})


def chat_refine(content, instruction, history):
    prompt = f"""
    You are a social media assistant.

    Original Content:
    {content}

    Previous conversation:
    {history}

    User request:
    {instruction}

    Improve the content accordingly.
    Return ONLY updated content.
    """
    response = llm.invoke(prompt)
    return response.content
import requests

import requests

# 🔐 Paste your OAuth access token here
ACCESS_TOKEN = "eyJraWQiOiJkOTI5NjY4YS1iYWIxLTRjNjktOTU5OC00MzczMTQ5NzIzZmYiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJodHRwczovL3d3dy5saW5rZWRpbi5jb20vb2F1dGgiLCJhdWQiOiI4Nm5zODN6a3VjaGNyciIsImlhdCI6MTc3NjMyNTcwMCwiZXhwIjoxNzc2MzI5MzAwLCJzdWIiOiJ6WmowcV9FeXN0IiwibmFtZSI6IkRpbWJ1IFNpdmEgUmFtIE1BTlVQQVRJIiwiZ2l2ZW5fbmFtZSI6IkRpbWJ1IFNpdmEgUmFtIiwiZmFtaWx5X25hbWUiOiJNQU5VUEFUSSIsImVtYWlsIjoibWFudXBhdGlzaXZhcmFtQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjoidHJ1ZSIsImxvY2FsZSI6ImVuX1VTIn0.s7Ha29ix8Ip1KGQgsMZmrKodW3QTUlWmaVFepbg8mBw26yxLa0_-Aab1xeRfrNSn2V6TFuzHGhSrhVGiRZlBNk7Ku8z_ciyji6Imtu_NFmogLh1XthXINR6Q8-UCgyOUusdG77PaKm50JP1sBABDdPXH-grODc5W_KO66npVlTtYbBxyfUGqlE_huC39ThuXmCNl7Ta-Yts9ailU8PMt8-lsGv28BzT21vHmP6tdsHhibEMeRzgOLlf9PixJOtajPRLxcKae4epM6QmafL2hCStHNyTkcYHgmVm5JfquGLklTGo_wA_yfw0izvwUVXkgCI6jos1zjDilWJ4k6WrJ3TdhR5mrAFdABxC8AcayDc0UtRzhMFpIYKQptyAOGKGtjYv_BeD9V-16acl7PGJRf1lhU53quEOOhnU00279rEjMhILvw8Ti3cMmzU025MuVjXeHb7Sp5bOTm3ToqsZE_bZ9hyqnphwO9LdUrCJBp4vaZ1TmZqKI-mqQvYSD8Yttx6qoHJVywbB1tk7QOcxZoD7fJppzrx9Aiws5YThRi0vaXJyZhTvhUVMeTVrA2ClgFQQHaJkEN1FUDDE7upi3FIvTEYPVd5NzrXKgy8QZOO27IOUhzz6ZXpTY6z4e2Rg8kRRLJ0_j3b6EonZxMBC8Jq1VoZ3R1eFizBhpfURyvFU"

# ✅ Your Member ID (already extracted)
MEMBER_ID = "zZj0q_Eyst"


def post_to_linkedin(content):
    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }

    data = {
        "author": f"urn:li:member:{MEMBER_ID}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    res = requests.post(url, headers=headers, json=data)

    print("\nSTATUS:", res.status_code)
    print("RESPONSE:", res.text)

    return res.status_code, res.text


# 🚀 TEST POST
if __name__ == "__main__":
    content = "🚀 Hello LinkedIn! My first API post is live 🔥"
    post_to_linkedin(content)
def post_to_twitter(content, bearer_token):
    url = "https://api.twitter.com/2/tweets"

    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }

    data = {
        "text": content
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()


import requests

def post_to_instagram(content, access_token, ig_user_id, image_url):
    # Step 1: create media container
    url = f"https://graph.facebook.com/v19.0/{ig_user_id}/media"

    params = {
        "image_url": image_url,
        "caption": content,
        "access_token": access_token
    }

    res = requests.post(url, data=params)
    creation_id = res.json().get("id")

    if not creation_id:
        return {"error": "Failed to create media", "response": res.json()}

    # Step 2: publish media
    publish_url = f"https://graph.facebook.com/v19.0/{ig_user_id}/media_publish"

    publish_params = {
        "creation_id": creation_id,
        "access_token": access_token
    }

    response = requests.post(publish_url, data=publish_params)

    return response.json()