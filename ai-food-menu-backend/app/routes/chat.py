from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from context_object.menu_context import MenuContextBuilder
from llm.prompt_builder import MenuPromptBuilder
from llm.llm_client import LLMClient
from app.services.ai_logger import log_ai_interaction

# ✅ Router MUST be defined before decorators
router = APIRouter()


# ----------------------------
# Request schema
# ----------------------------
class ChatRequest(BaseModel):
    question: str


# ----------------------------
# Chat route
# ----------------------------
@router.post("/menu/{slug}/chat")
def chat_about_menu_item(slug: str, payload: ChatRequest):
    """
    LLM-powered chat about a menu item using slug-based routing.
    """

    try:
        # 1️⃣ Build DB-backed context
        context = MenuContextBuilder.get_menu_context(slug)

        # 2️⃣ Build prompt (RAG)
        prompt = MenuPromptBuilder.build_prompt({
            "menu": context["menu"],
            "ingredients": context["ingredients"],
            "user_question": payload.question,
        })

        # 3️⃣ Call LLM
        response = LLMClient.generate(prompt)

        # 4️⃣ Log interaction
        log_ai_interaction(
            menu_id=context["menu"]["menu_id"],
            prompt=prompt,
            response=response,
            freshness_score=None,
            risk_level=None,
        )

        return {"text": response}

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        print("CHAT ERROR:", e)
        raise HTTPException(
            status_code=500,
            detail="Failed to generate chat response"
        )
