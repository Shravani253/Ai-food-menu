from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio
import os

_llm = None


def ensure_event_loop():
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)


def get_llm():
    global _llm

    if _llm is None:
        ensure_event_loop()
        
        # 🔑 Get key INSIDE function to ensure we catch the .env load result
        api_key = os.getenv("GEMINI_API_KEY")
        print(f"DEBUG LLM: Using key starting with {api_key[:8] if api_key else 'NONE'}")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in environment variables.")

        _llm = ChatGoogleGenerativeAI(
            model="models/gemini-flash-latest",
            google_api_key=api_key,
            temperature=0.2,
        )

    return _llm
