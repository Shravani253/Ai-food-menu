from langchain_core.messages import HumanMessage
from llm.llm_provider import get_llm


class LLMClient:
    """
    Stateless LLM client wrapper.
    Safe to call from anywhere in the backend.
    """

    @staticmethod
    def generate(prompt: str) -> str:
        llm = get_llm()

        response = llm.invoke(
            [HumanMessage(content=prompt)]
        )

        content = response.content

        # 🔑 Gemini may return list OR string
        if isinstance(content, list):
            text_parts = []
            for block in content:
                if isinstance(block, dict) and "text" in block:
                    text_parts.append(block["text"])
                elif hasattr(block, "text"):
                    text_parts.append(block.text)

            return "\n".join(text_parts).strip()

        # fallback (string)
        return str(content).strip()
