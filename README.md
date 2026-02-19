# 🍽️ AI Food Menu — Freshness, Safety & Trust.

An **AI-powered restaurant menu system** that dynamically adapts based on **ingredient freshness, storage conditions, and real human feedback (RLHF)**.

Built for transparency, food safety, and customer trust.

---

## 🚀 What This Project Does

This system replaces a static restaurant menu with a **living, intelligent menu** that:

- Shows **real-time food availability & freshness**
- Explains *why* a dish is safe (or not) using AI
- Lets users **chat with an AI** about their food
- Learns from **human feedback (RLHF)** to improve future responses
- Adapts menu visibility based on freshness signals

---

## 🧠 Core Features

### ✅ Dynamic Menu Decisions
- Menu items are **enabled / disabled** based on:
  - Ingredient freshness
  - Risk level
  - Storage conditions
- Decisions happen **server-side**, not via frontend logic

### 🤖 AI Food Insight (LLM + RAG)
- Each dish has an AI explanation:
  - Ingredient freshness
  - Safety considerations
  - Availability reasoning
- Powered by **Gemini (via LangChain)**

### 💬 Dish-Level Chatbot
- Users can ask:
  - “Is this safe today?”
  - “Why is this marked fresh?”
- Chat uses **real menu + ingredient context (RAG)**

### 🧪 RLHF (Human Feedback Loop)
- Users **must submit written feedback**
- Feedback is:
  - Parsed using NLP
  - Logged to database
  - Used to adapt AI tone and clarity
- Enables learning **without compromising safety**

---

## 🏗️ Architecture Overview

Frontend (React + Vite)
│
├── Menu Page (Category-wise)
├── Dish Detail Page
│ ├── AI Insight
│ └── Chatbot + Feedback
│
Backend (FastAPI)
│
├── routes/
│ ├── menu.py → Menu listing
│ ├── insight.py → AI food explanation
│ ├── chat.py → Dish chatbot (RAG)
│ └── feedback.py → Human feedback intake
│
├── context_object/
│ └── menu_context.py
│
├── llm/
│ ├── llm_client.py
│ ├── llm_provider.py
│ └── prompt_builder.py
│
├── rlhf/
│ └── feedback_analyzer.py
│
└── services/
├── postgres.py
├── ai_logger.py
└── feedback_logger.py


---

## 🛠️ Tech Stack

### Frontend
- React + TypeScript
- Vite
- CSS (lightweight & fast)

### Backend
- FastAPI
- PostgreSQL
- LangChain
- Google Gemini
- psycopg2

---

## ⚙️ Setup Instructions

### 1️⃣ Backend Setup

```bash
cd ai-food-menu-backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

To Run and see the demo of live application 

Backend runs on:

https://ai-food-menu.onrender.com

2️⃣ Frontend Setup
cd frontend
npm install
npm run dev


Frontend runs on:

https://ai-food-menu.vercel.app/

🔁 How RLHF Works

User chats with the AI about a dish
After interaction, written feedback is required

Feedback is:
Parsed into sentiment & tags

Logged to database

Aggregated feedback influences:

AI tone

Detail level

Safety emphasis

Safety rules are never overridden by feedback.

🧪 How to Test Learning

Chat with multiple dishes

Submit feedback (positive & negative)

Check database tables:

feedback_logs

ai_interactions

Restart backend and observe AI tone changes

🔐 Safety by Design

AI cannot enable unsafe dishes

Freshness logic is authoritative

All AI interactions are logged

Feedback affects communication, not safety thresholds

🏁 Project Status

✅ Backend complete
✅ Frontend complete
✅ AI Chat working
✅ RLHF pipeline active
✅ Hackathon-ready

🌟 Why This Matters

Food safety systems today are:

Static
Opaque
Trust-based

This project makes food explainable, adaptive, and accountable.

Built with ❤️ for trust, transparency, and safer dining.
