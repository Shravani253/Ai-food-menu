from fastapi import APIRouter, HTTPException
import re
from psycopg2.extras import RealDictCursor

from context_object.menu_context import MenuContextBuilder
from context_object.freshness_engine import FreshnessEngine
from app.domain.menu_decision_engine import decide_menu_item
from app.services.postgres import get_db_connection

router = APIRouter()
SCHEMA = "public"


# ----------------------------
# Helpers
# ----------------------------

def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


# ----------------------------
# GET FULL MENU
# ----------------------------

@router.get("/menu")
def get_menu():
    """
    Returns all menu items with LIVE freshness status.
    """

    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB unavailable")

    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cur.execute(
            f"""
            SELECT
                menu_id,
                name,
                category,
                price,
                is_available
            FROM {SCHEMA}.menu_items
            ORDER BY category, name
            """
        )

        menu_items = cur.fetchall()
        final_menu = []

        for item in menu_items:
            slug = slugify(item["name"])

            # 1️⃣ Build DB context
            context = MenuContextBuilder.get_menu_context(slug)

            # 2️⃣ Freshness evaluation
            freshness_report = FreshnessEngine.score_menu(context)

            # 3️⃣ Decision engine
            decided = decide_menu_item(
                menu=item,
                freshness={
                    "score": freshness_report["menu_freshness"],
                    "risk_level": freshness_report["status"],
                },
                feedback=None,
            )

            decided["id"] = slug
            decided["last_checked"] = freshness_report["evaluated_at"]

            final_menu.append(decided)

        return final_menu

    finally:
        cur.close()
        conn.close()


# ----------------------------
# GET SINGLE MENU ITEM (Page 2)
# ----------------------------

@router.get("/menu/{slug}")
def get_menu_item(slug: str):
    """
    Returns a single menu item for Dish Detail Page
    """

    try:
        context = MenuContextBuilder.get_menu_context(slug)
        freshness = FreshnessEngine.score_menu(context)

        return {
            "id": slug,
            "name": context["menu"]["name"],
            "category": context["menu"]["category"],
            "price": context["menu"]["price"],
            "status": freshness["status"],
            "last_checked": freshness["evaluated_at"],
        }

    except ValueError:
        raise HTTPException(status_code=404, detail="Menu item not found")
