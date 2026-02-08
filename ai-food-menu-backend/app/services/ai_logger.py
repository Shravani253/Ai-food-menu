from app.services.postgres import get_db_connection
from datetime import datetime
import json


# -------------------------
# Freshness logging
# -------------------------

def log_freshness(
    menu_id: int,
    ingredient_id: int,
    freshness_score: float,
    risk_level: str,
    factors: dict,
):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO freshness_logs (
            menu_id,
            ingredient_id,
            freshness_score,
            risk_level,
            factors,
            created_at
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            menu_id,
            ingredient_id,
            freshness_score,
            risk_level,
            json.dumps(factors),
            datetime.utcnow(),
        )
    )

    conn.commit()
    cur.close()
    conn.close()


# -------------------------
# AI interaction logging
# -------------------------

def log_ai_interaction(
    menu_id: int,
    prompt: str,
    response: str,
    freshness_score: float,
    risk_level: str,
):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO ai_interactions (
            menu_id,
            model_name,
            prompt,
            response,
            freshness_score,
            risk_level,
            created_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            menu_id,
            "gemini-flash",
            prompt,
            response,
            freshness_score,
            risk_level,
            datetime.utcnow(),
        )
    )

    conn.commit()
    cur.close()
    conn.close()


# -------------------------
# Storage condition logging
# -------------------------

def upsert_storage_condition(
    ingredient_id: int,
    storage_type: str,
    temperature: float,
    humidity: float,
):
    """
    Called periodically (e.g., every 5 hours)
    to record real storage state.
    """

    deviation_flag = False

    if storage_type == "Chiller" and temperature > 5:
        deviation_flag = True
    if storage_type == "Freezer" and temperature > -10:
        deviation_flag = True

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO storage_conditions (
            ingredient_id,
            storage_type,
            temperature,
            humidity,
            last_checked,
            deviation_flag
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            ingredient_id,
            storage_type,
            temperature,
            humidity,
            datetime.utcnow(),
            deviation_flag,
        )
    )

def log_feedback(
    menu_id,
    feedback_text,
    sentiment,
    tags,
    confidence
):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO feedback_logs (
            menu_id,
            feedback_text,
            sentiment,
            tags,
            confidence,
            created_at
        )
        VALUES (%s, %s, %s, %s, %s, NOW())
        """,
        (
            menu_id,
            feedback_text,
            sentiment,
            tags,
            confidence,
        )
    )

    conn.commit()
    cur.close()
    conn.close()



