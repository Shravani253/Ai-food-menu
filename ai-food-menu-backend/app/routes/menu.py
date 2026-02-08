from fastapi import APIRouter
import re

from app.domain.menu_decision_engine import decide_menu_item

router = APIRouter()


# ---------- helpers ----------

def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


# ---------- routes ----------

@router.get("/menu")
def get_menu():
    """
    Returns MENU ITEMS (not ingredients)

    - Data is hardcoded (for now)
    - `status`, `availability` added via decision engine
    - `id` (slug) is used by frontend to resolve images
    """

    menu_items = [
        # SEAFOOD (8)
        {"menu_id": 1, "name": "Grilled Salmon", "category": "Seafood", "price": 750},
        {"menu_id": 2, "name": "Prawn Masala", "category": "Seafood", "price": 680},
        {"menu_id": 3, "name": "Tuna Steak", "category": "Seafood", "price": 820},
        {"menu_id": 4, "name": "Crab Curry", "category": "Seafood", "price": 790},
        {"menu_id": 5, "name": "Squid Fry", "category": "Seafood", "price": 620},
        {"menu_id": 6, "name": "Pomfret Tawa Fry", "category": "Seafood", "price": 700},
        {"menu_id": 7, "name": "Lobster Thermidor", "category": "Seafood", "price": 1400},
        {"menu_id": 8, "name": "Clam Soup", "category": "Seafood", "price": 450},

        # CHICKEN (6)
        {"menu_id": 9, "name": "Grilled Chicken", "category": "Chicken", "price": 520},
        {"menu_id": 10, "name": "Chicken Curry", "category": "Chicken", "price": 560},
        {"menu_id": 11, "name": "Butter Chicken", "category": "Chicken", "price": 620},
        {"menu_id": 12, "name": "Chicken Wings", "category": "Chicken", "price": 480},
        {"menu_id": 13, "name": "Chicken Biryani", "category": "Chicken", "price": 650},
        {"menu_id": 14, "name": "Chicken Soup", "category": "Chicken", "price": 350},

        # VEG (6)
        {"menu_id": 15, "name": "Veg Stir Fry", "category": "Veg", "price": 420},
        {"menu_id": 16, "name": "Paneer Tikka", "category": "Veg", "price": 520},
        {"menu_id": 17, "name": "Veg Curry", "category": "Veg", "price": 450},
        {"menu_id": 18, "name": "Mushroom Masala", "category": "Veg", "price": 480},
        {"menu_id": 19, "name": "Veg Biryani", "category": "Veg", "price": 500},
        {"menu_id": 20, "name": "Creamy Spinach", "category": "Veg", "price": 460},
    ]

    final_menu = []

    for item in menu_items:
        freshness = {
            "score": 85,
            "risk_level": "Low"
        }

        decided = decide_menu_item(
            menu=item,
            freshness=freshness,
            feedback=None
        )

        decided["id"] = slugify(decided["name"])
        final_menu.append(decided)

    return final_menu


# ---------- DETAIL ROUTE (FOR CLICK PAGE) ----------

@router.get("/menu/{slug}")
def get_menu_item(slug: str):
    """
    Returns SINGLE MENU ITEM details
    Used by Dish Detail Page
    """

    name = slug.replace("-", " ").title()

    return {
        "id": slug,
        "name": name,
        "category": "Veg",
        "status": "Fresh",
        "last_checked": "45 minutes ago"
    }
