from llm.llm_client import LLMClient

client = LLMClient()

try:
    response = client.generate("Explain food freshness in one line.")
    print("Gemini Response:", response)
except Exception as e:
    print("Gemini Error:", e)
