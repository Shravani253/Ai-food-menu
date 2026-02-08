from fastapi import APIRouter
from pydantic import BaseModel

from rlhf.feedback_analyzer import FeedbackAnalyzer
from app.services.ai_logger import log_feedback

router = APIRouter()


# ----------------------------
# Request schema
# ----------------------------

class FeedbackRequest(BaseModel):
    text: str


# ----------------------------
# Routes
# ----------------------------

@router.post("/menu/{menu_id}/feedback")
def submit_feedback(menu_id: str, payload: FeedbackRequest):
    """
    Receives human feedback from frontend (chatbot / feedback UI)
    """

    # 1️⃣ Analyze feedback (NLP + RL signal)
    analysis = FeedbackAnalyzer.analyze(payload.text)

    # 2️⃣ Persist feedback for RLHF + auditing
    log_feedback(
        menu_id=menu_id,
        feedback_text=payload.text,
        sentiment=analysis["sentiment"],
        tags=analysis["tags"],
        confidence=analysis["confidence"],
    )

    return {
        "status": "ok",
        "analysis": analysis
    }
