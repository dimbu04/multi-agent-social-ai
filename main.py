import os
import time
import requests
import certifi

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from typing import TypedDict

from langchain_groq import ChatGroq
from langgraph.graph import StateGraph

load_dotenv()


# ---------------- LLM ----------------

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=os.getenv("OPENAI_API_KEY")
)


def safe_invoke(prompt):
    for _ in range(3):
        try:
            return llm.invoke(prompt)
        except Exception:
            time.sleep(10)
    raise Exception("LLM failed")


# ---------------- SCRAPER ----------------

def scraper_agent(state):

    response = requests.get(
        state["url"],
        verify=certifi.where(),
        timeout=20
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    content = " ".join(
        [p.text for p in soup.find_all("p")][:50]
    )

    return {
        "scraped_content": content
    }


# ---------------- SUMMARY ----------------

def summarize_agent(state):

    prompt=f"""
Summarize this content clearly:

{state["scraped_content"]}
"""

    res=safe_invoke(prompt)

    return {
        "summary":res.content
    }


# ---------------- STRATEGY ----------------

def planner_agent(state):

    prompt=f"""
Create a social media strategy from:

{state["summary"]}

Return:
- key message
- audience
- content angle
"""

    res=safe_invoke(prompt)

    return {
        "strategy":res.content
    }



# ---------------- PLATFORM AGENTS ----------------

def linkedin_agent(state):

    prompt=f"""
Write professional LinkedIn post:

- Hook
- Value
- CTA
- 5 hashtags

ONLY return post.

{state["strategy"]}
"""

    res=safe_invoke(prompt)

    return {
        "linkedin":res.content
    }



def twitter_agent(state):

    prompt=f"""
Write engaging Twitter/X post

-Max 280 chars
-Hook
-2 hashtags max

ONLY return tweet

{state["strategy"]}
"""

    res=safe_invoke(prompt)

    return {
        "twitter":res.content
    }



def instagram_agent(state):

    prompt=f"""
Write Instagram caption:

-Engaging caption
-CTA
-5 hashtags

ONLY return caption

{state["strategy"]}
"""

    res=safe_invoke(prompt)

    return {
        "instagram":res.content
    }



# ---------------- STATE ----------------

class GraphState(TypedDict):
    url:str
    scraped_content:str
    summary:str
    strategy:str
    linkedin:str
    twitter:str
    instagram:str



# ---------------- PIPELINE ----------------

def run_pipeline(url,platform):

    workflow=StateGraph(GraphState)

    workflow.add_node(
        "scraper",
        scraper_agent
    )

    workflow.add_node(
        "summarizer",
        summarize_agent
    )

    workflow.add_node(
        "planner",
        planner_agent
    )

    workflow.set_entry_point("scraper")

    workflow.add_edge(
        "scraper",
        "summarizer"
    )

    workflow.add_edge(
        "summarizer",
        "planner"
    )


    if platform=="LinkedIn":

        workflow.add_node(
            "linkedin",
            linkedin_agent
        )

        workflow.add_edge(
            "planner",
            "linkedin"
        )

        workflow.set_finish_point(
            "linkedin"
        )


    elif platform=="Twitter":

        workflow.add_node(
            "twitter",
            twitter_agent
        )

        workflow.add_edge(
            "planner",
            "twitter"
        )

        workflow.set_finish_point(
            "twitter"
        )


    elif platform=="Instagram":

        workflow.add_node(
            "instagram",
            instagram_agent
        )

        workflow.add_edge(
            "planner",
            "instagram"
        )

        workflow.set_finish_point(
            "instagram"
        )


    elif platform=="All":

        workflow.add_node(
            "linkedin",
            linkedin_agent
        )

        workflow.add_node(
            "twitter",
            twitter_agent
        )

        workflow.add_node(
            "instagram",
            instagram_agent
        )

        workflow.add_edge(
            "planner",
            "linkedin"
        )

        workflow.add_edge(
            "planner",
            "twitter"
        )

        workflow.add_edge(
            "planner",
            "instagram"
        )

        workflow.set_finish_point(
            "instagram"
        )


    app=workflow.compile()

    return app.invoke(
        {"url":url}
    )



# ---------------- CHAT REFINE ----------------

def chat_refine(content,instruction,history):

    prompt=f"""
Improve this content:

{content}

Instruction:
{instruction}
"""

    res=safe_invoke(prompt)

    return res.content