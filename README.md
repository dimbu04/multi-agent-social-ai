# 🚀 Multi-Agent Social Media AI

An AI-powered system that automatically generates and publishes social media content using a multi-agent architecture.

---

## 🔥 Project Overview

This project takes a blog URL and:

- Scrapes content from the web
- Generates AI-based posts
- Creates images dynamically
- Refines content
- Publishes to LinkedIn, Twitter, Instagram

---

## 🧠 Architecture (LangGraph Style)

![Architecture](diagram.png)

### Flow:

START  
↓  
scraper_agent (Playwright)  
↓  
content_agent (Groq AI)  
↙        ↘  
image_agent (Pillow)   refiner_agent (Groq AI)  
↘        ↙  
publisher_agent (Playwright)  
↓  
END  

---

## ⚙️ Tech Stack

- LangChain
- LangGraph
- Groq AI (LLM)
- Playwright (Automation)
- Pillow (Image generation)
- Streamlit (UI)
- AWS EC2 (Deployment)

---

## ☁️ AWS Deployment

The application is deployed on AWS EC2 for real-time access.

### Steps:

1. Created EC2 instance (Ubuntu)
2. Connected via SSH
3. Cloned GitHub repo
4. Installed dependencies
5. Set environment variables (.env)
6. Ran Streamlit app

```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
