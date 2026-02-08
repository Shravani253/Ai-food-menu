from typing import Dict
from rlhf.feedback_analyzer import FeedbackAnalyzer


class MenuPromptBuilder:
    """
    Unified prompt builder for:
    1) Menu Insight (freshness-based)
    2) Menu Chat (RAG-based Q&A)

    Backward-compatible with insight.py
    """

    @staticmethod
    def build_prompt(payload: Dict) -> str:
        # 🔹 RLHF tone modifiers (safe default)
        style = FeedbackAnalyzer.get_prompt_modifiers()

        lines = []

        # 🔹 System framing
        lines.append(
            "You are a food safety assistant for a restaurant menu.\n"
            "Explain information clearly, calmly, and honestly.\n"
            "Do NOT exaggerate or give medical advice.\n"
        )

        if style.get("tone") == "simple":
            lines.append(
                "Use simple, non-technical language that customers can easily understand."
            )

        if style.get("safety_emphasis", False):
            lines.append(
                "If food is unsafe or unavailable, clearly state this first."
            )

        lines.append("")

        # --------------------------------------------------
        # CASE 1️⃣: INSIGHT FLOW (existing insight.py)
        # --------------------------------------------------
        if "overall_freshness" in payload:
            menu = payload["menu"]

            lines.append(f"Menu Item: {menu['name']}")
            lines.append(f"Category: {menu['category']}")
            lines.append(f"Price: ₹{menu['price']}")
            lines.append(
                f"Availability: {'Available' if menu['is_available'] else 'Unavailable'}"
            )

            lines.append("")
            lines.append(
                f"Overall Freshness Score: {payload['overall_freshness']}/100"
            )
            lines.append(
                f"Overall Risk Level: {payload['overall_risk']}"
            )

            lines.append("\nIngredient Details:")
            for ing in payload.get("ingredients", []):
                lines.append(
                    f"- {ing['name']}: "
                    f"{ing.get('final_freshness', ing.get('freshness_score', 'N/A'))}/100 "
                    f"(Risk: {ing['risk_level']})"
                )

                for w in ing.get("warnings", []):
                    lines.append(f"  ⚠ {w}")

            lines.append(
                "\nExplain the above information in a friendly, customer-facing way. "
                "Keep it short, transparent, and confidence-building."
            )

            return "\n".join(lines)

        # --------------------------------------------------
        # CASE 2️⃣: CHAT FLOW (menu/{slug}/chat)
        # --------------------------------------------------
        menu = payload["menu"]
        ingredients = payload.get("ingredients", [])
        user_question = payload.get("user_question", "")

        lines.append(f"Menu Item: {menu['name']}")
        lines.append(f"Category: {menu['category']}")
        lines.append(f"Price: ₹{menu['price']}")
        lines.append(
            f"Availability: {'Available' if menu['is_available'] else 'Unavailable'}"
        )

        lines.append("\nIngredients:")
        for ing in ingredients:
            lines.append(
                f"- {ing['name']} "
                f"(Freshness: {ing['freshness_score']}, Risk: {ing['risk_level']})"
            )

        lines.append("")
        lines.append(f"Customer question: {user_question}")

        lines.append(
            "\nAnswer the customer's question clearly and confidently, "
            "using the information above. Be concise and reassuring."
        )

        return "\n".join(lines)
