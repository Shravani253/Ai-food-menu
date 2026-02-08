from datetime import datetime
from app.services.postgres import get_db_connection


def log_human_feedback(
    menu_id: int,
    sentiment: float,
    tags: list,
    confidence: float,
    raw_text: str,
):
    """
    Stores raw human feedback for RLHF.

    Called AFTER feedback_analyser.analyze().
    This function has NO intelligence — it only logs.
    """

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO feedback_logs (
            menu_id,
            sentiment,
            tags,
            confidence,
            raw_text,
            created_at
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            menu_id,
            sentiment,
            tags,
            confidence,
            raw_text,
            datetime.utcnow(),
        )
    )

    conn.commit()
    cur.close()
    conn.close()
