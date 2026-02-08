from datetime import datetime, date
from typing import Dict, List, Tuple


class FreshnessEngine:
    """
    Deterministic freshness scoring engine.
    Computes and explains WHY a food item is fresh, risky, or unsafe.
    """

    # ---------- helpers ----------

    @staticmethod
    def _days_between(start: date, end: date) -> int:
        """Return non-negative day difference."""
        return max((end - start).days, 0)

    @staticmethod
    def _safe_temp_range(category: str) -> Tuple[int, int]:
        """
        Safe storage temperature ranges (°C)
        """
        return {
            "Seafood": (0, 4),
            "Chicken": (0, 4),
            "Meat": (0, 4),
            "Vegetarian": (2, 8),
            "Dairy": (2, 6),
        }.get(category, (0, 8))

    # ---------- ingredient scoring ----------

    @classmethod
    def score_ingredient(cls, ingredient: Dict) -> Dict:
        """
        Compute freshness score for a single ingredient.
        """

        today = datetime.utcnow().date()

        received: date = ingredient["received_date"]
        expiry: date = ingredient["expiry_date"]

        total_life = cls._days_between(received, expiry)
        remaining_life = cls._days_between(today, expiry)

        # Base freshness from shelf life
        if total_life == 0:
            base_score = 0.0
        else:
            base_score = round((remaining_life / total_life) * 100, 2)

        warnings: List[str] = []
        penalty = 0

        # Expiry checks
        if remaining_life <= 0:
            warnings.append("Ingredient expired")
            penalty += 50
        elif remaining_life <= 1:
            warnings.append("Ingredient near expiry")
            penalty += 20

        # Temperature check (latest event only)
        event = ingredient.get("latest_event")
        if event and event.get("event_type") == "storage_check":
            temp = event.get("event_value", {}).get("temp")
            min_t, max_t = cls._safe_temp_range(ingredient["category"])

            if temp is not None and not (min_t <= temp <= max_t):
                warnings.append(
                    f"Unsafe storage temperature detected ({temp}°C)"
                )
                penalty += 15

        # Risk weighting
        risk_level = ingredient.get("risk_level", "Low")
        if risk_level == "Medium":
            penalty += 10
        elif risk_level == "High":
            penalty += 25

        final_score = max(round(base_score - penalty, 2), 0.0)

        return {
            "ingredient_id": ingredient["ingredient_id"],
            "name": ingredient["name"],
            "final_freshness": final_score,
            "base_freshness": base_score,
            "penalty": penalty,
            "warnings": warnings,
        }

    # ---------- menu scoring ----------

    @classmethod
    def score_menu(cls, context: Dict) -> Dict:
        """
        Compute freshness score for an entire menu item.
        Uses the weakest ingredient as the deciding factor.
        """

        ingredient_results: List[Dict] = []
        min_score = 100.0
        all_warnings: List[str] = []

        for ingredient in context["ingredients"]:
            result = cls.score_ingredient(ingredient)
            ingredient_results.append(result)

            min_score = min(min_score, result["final_freshness"])
            all_warnings.extend(result["warnings"])

        # Menu-level status
        if min_score < 40:
            status = "Unsafe"
        elif min_score < 70:
            status = "Caution"
        else:
            status = "Fresh"

        return {
            "menu_id": context["menu"]["menu_id"],
            "menu_name": context["menu"]["name"],
            "menu_freshness": round(min_score, 2),
            "status": status,
            "warnings": list(set(all_warnings)),
            "ingredients": ingredient_results,
            "evaluated_at": datetime.utcnow().isoformat(),
        }
