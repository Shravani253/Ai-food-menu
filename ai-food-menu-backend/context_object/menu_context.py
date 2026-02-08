from datetime import datetime
from psycopg2.extras import RealDictCursor
from app.services.postgres import get_db_connection

SCHEMA = "public"


class MenuContextBuilder:
    """
    Builds a structured, backend-only context object for a menu item.

    Used by:
    - freshness_engine
    - menu_decision_engine
    - LLM / RAG reasoning

    Slug-based input (e.g. 'grilled-salmon').
    """

    @staticmethod
    def get_menu_context(slug: str) -> dict:
        conn = get_db_connection()
        if not conn:
            raise RuntimeError("Database connection not available")

        cur = conn.cursor(cursor_factory=RealDictCursor)

        try:
            # 1️⃣ Resolve slug → menu item
            cur.execute(
                f"""
                SELECT
                    menu_id,
                    name,
                    category,
                    price,
                    is_available
                FROM {SCHEMA}.menu_items
                WHERE slug = %s
                """,
                (slug,)
            )
            menu = cur.fetchone()

            if not menu:
                raise ValueError(f"Menu item not found for slug='{slug}'")

            menu_id = menu["menu_id"]

            # 2️⃣ Fetch ingredients linked to menu_id
            cur.execute(
                f"""
                SELECT
                    i.ingredient_id,
                    i.name,
                    i.category,
                    i.received_date,
                    i.expiry_date,
                    i.freshness_score,
                    i.risk_level
                FROM {SCHEMA}.ingredients i
                JOIN {SCHEMA}.menu_ingredients mi
                    ON i.ingredient_id = mi.ingredient_id
                WHERE mi.menu_id = %s
                """,
                (menu_id,)
            )
            ingredients = cur.fetchall()

            # 3️⃣ Fetch latest event per ingredient (optional)
            ingredient_events = {}

            for ingredient in ingredients:
                cur.execute(
                    f"""
                    SELECT
                        event_type,
                        event_value,
                        created_at
                    FROM {SCHEMA}.ingredient_events
                    WHERE ingredient_id = %s
                    ORDER BY created_at DESC
                    LIMIT 1
                    """,
                    (ingredient["ingredient_id"],)
                )
                ingredient_events[ingredient["ingredient_id"]] = cur.fetchone()

            # 4️⃣ Build final context object
            context = {
                "menu": {
                    "menu_id": menu["menu_id"],
                    "slug": slug,
                    "name": menu["name"],
                    "category": menu["category"],
                    "price": menu["price"],
                    "is_available": menu["is_available"],
                },
                "ingredients": [],
                "generated_at": datetime.utcnow().isoformat(),
            }

            for ingredient in ingredients:
                context["ingredients"].append({
                    "ingredient_id": ingredient["ingredient_id"],
                    "name": ingredient["name"],
                    "category": ingredient["category"],
                    "received_date": ingredient["received_date"],
                    "expiry_date": ingredient["expiry_date"],
                    "freshness_score": ingredient["freshness_score"],
                    "risk_level": ingredient["risk_level"],
                    "latest_event": ingredient_events.get(
                        ingredient["ingredient_id"]
                    ),
                })

            return context

        finally:
            cur.close()
            conn.close()
