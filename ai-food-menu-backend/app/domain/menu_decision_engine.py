from typing import Dict, List


def decide_menu_item(
    menu: Dict,
    freshness: Dict,
    feedback: Dict | None = None,
) -> Dict:
    """
    Core decision engine.

    Takes raw signals and returns frontend-ready menu state.
    """

    # -------------------------
    # 1. Availability (SAFETY)
    # -------------------------
    freshness_score = freshness["score"]

    if freshness_score < 60:
        availability = "UNAVAILABLE"
        status = "Unavailable"
    elif freshness_score < 75:
        availability = "LIMITED"
        status = "Caution"
    else:
        availability = "AVAILABLE"
        status = "Fresh"

    # -------------------------
    # 2. Priority (ordering)
    # -------------------------
    priority = 1  # base priority (lower = higher in UI)

    if feedback:
        if feedback["avg_sentiment"] < -0.4:
            priority += 2
        if feedback["negative_ratio"] > 0.6:
            priority += 1

    # -------------------------
    # 3. Warnings (UX hints)
    # -------------------------
    warnings: List[str] = []

    if feedback and "oil" in feedback.get("dominant_tags", []):
        warnings.append("May feel heavy")

    if feedback and "spice" in feedback.get("dominant_tags", []):
        warnings.append("Spicy for some")

    # -------------------------
    # 4. Final shape (FRONTEND)
    # -------------------------
    return {
        "id": menu["menu_id"],
        "name": menu["name"],
        "category": menu["category"],
        "price": menu["price"],

        "availability": availability,
        "status": status,
        "priority": priority,
        "warnings": warnings,
    }
