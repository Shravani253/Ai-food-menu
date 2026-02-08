import re
from typing import Dict, List


class FeedbackAnalyzer:
    """
    Stateless RLHF signal extractor.

    Takes raw human feedback text and converts it into
    structured signals for later aggregation.
    """

    NEGATIVE_KEYWORDS = {
        "oil": ["oily", "greasy", "too much oil"],
        "spice": ["too spicy", "burning", "hot"],
        "taste": ["bad taste", "bland", "tasteless"],
        "texture": ["rubbery", "hard", "overcooked", "undercooked"],
        "freshness": ["stale", "not fresh", "smelly", "spoiled"],
    }

    POSITIVE_KEYWORDS = [
        "good",
        "tasty",
        "delicious",
        "fresh",
        "perfect",
        "loved",
        "nice",
    ]

    @staticmethod
    def analyze(text: str) -> Dict:
        """
        Analyze raw human feedback.

        Returns:
        {
            "sentiment": float,   # -1.0 → 1.0
            "tags": list[str],    # issue categories
            "confidence": float   # extraction confidence
        }
        """

        if not text or not text.strip():
            return {
                "sentiment": 0.0,
                "tags": [],
                "confidence": 0.0,
            }

        text = text.lower().strip()

        sentiment_score = 0.0
        hit_count = 0
        tags: List[str] = []

        # Detect negative signals
        for tag, keywords in FeedbackAnalyzer.NEGATIVE_KEYWORDS.items():
            for kw in keywords:
                if kw in text:
                    tags.append(tag)
                    sentiment_score -= 0.3
                    hit_count += 1
                    break

        # Detect positive signals
        for kw in FeedbackAnalyzer.POSITIVE_KEYWORDS:
            if re.search(rf"\b{kw}\b", text):
                sentiment_score += 0.2
                hit_count += 1

        # Clamp sentiment
        sentiment_score = max(-1.0, min(1.0, sentiment_score))

        # Confidence heuristic
        confidence = min(1.0, 0.3 + (0.15 * hit_count))

        return {
            "sentiment": round(sentiment_score, 2),
            "tags": list(set(tags)),
            "confidence": round(confidence, 2),
        }

    @staticmethod
    def get_prompt_modifiers() -> Dict:
        """
        Returns style modifiers based on aggregated feedback.
        TEMP: returns defaults until DB aggregation is implemented.
        """
        return {
            "tone": "friendly",
            "safety_emphasis": True
        }
