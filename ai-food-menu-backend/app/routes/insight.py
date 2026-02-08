from fastapi import APIRouter

from llm.prompt_builder import MenuPromptBuilder
from llm.llm_client import LLMClient
from app.services.ai_logger import log_ai_interaction

router = APIRouter()

@router.get("/menu/{slug}/insight")
def get_food_insight(slug: str):
    """
    TEMP insight endpoint (hardcoded menu, real LLM)
    """

   # TEMP slug → menu mapping
    menu = {
        "name": slug.replace("-", " ").title(),
        "category": "Veg",
        "price": 0,
        "is_available": True
    }

    # TEMP freshness report (until DB + scheduler)
    freshness_report = {
        "menu": menu,
        "overall_freshness": 85,
        "overall_risk": "Low",
        "ingredients": []
    }

    # ✅ Build prompt (THIS MATCHES YOUR FILE)
    prompt = MenuPromptBuilder.build_prompt(freshness_report)

    # Call LLM
    client = LLMClient()
    response = client.generate(prompt)

    # Log interaction (menu_id unknown for now)
    log_ai_interaction(
        menu_id=None,                # TEMP
        prompt=prompt,
        response=response,
        freshness_score=freshness_report["overall_freshness"],
        risk_level=freshness_report["overall_risk"]
    )

    return {
        "text": response
    }
