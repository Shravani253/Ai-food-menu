import os

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA

from llm.alerts_embeddings import generate_visual_alerts
from llm.alerts_embeddings import system_dashboard_summary



# ===============================
# Config
# ===============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")


# ===============================
# Load Vector DB
# ===============================

embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vectordb = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embedding_model
)

retriever = vectordb.as_retriever(search_kwargs={"k": 3})


# ===============================
# Load Gemini LLM
# ===============================

llm = ChatGoogleGenerativeAI(
    model="models/gemini-flash-latest",   # <-- Correct model name
    google_api_key=GEMINI_API_KEY,
    temperature=0.2
)


# ===============================
# RAG Chain
# ===============================

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True,
    chain_type="stuff"
)


# ===============================
# Fallback Mechanism
# ===============================

def fallback_response(query: str) -> str:
    return f"""
I could not find relevant traceability data for your question:

"{query}"

Possible reasons:
- Ingredient was never ingested
- No storage or transport data
- No dish consumption record

Try asking:
• "Which ingredients are expired?"
• "Is mozzarella cheese safe?"
• "Which ingredient is overused?"
• "Show risks in inventory"
""".strip()


def safe_rag_query(query: str) -> str:
    try:
        result = qa_chain.invoke({"query": query})

        answer = result["result"]
        docs = result["source_documents"]

        # Soft fallback
        if not docs:
            return fallback_response(query)

        return answer

    except Exception as e:
        # Hard fallback
        return f"""
⚠ AI system error:
{str(e)}

Falling back to system-safe mode.
Please try again or check your API key and internet connection.
""".strip()


# ===============================
# Terminal Chat Endpoint
# ===============================

def start_terminal_chat():
    print("\n🧠 Food Traceability AI Chatbot")
    print("Ask about freshness, expiry, overuse, risks.")
    print("Type 'exit', 'quit', or 'bye' to stop.\n")

    while True:
        user_input = input("🧑 You: ").strip()

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("👋 Chat ended. Stay safe with your food!")
            break

        if not user_input:
            print("⚠ Please ask a valid question.\n")
            continue

        print("\n🤖 AI thinking...\n")
        response = safe_rag_query(user_input)
        print("🤖 AI:", response, "\n")


# ===============================
# Run
# ===============================

if __name__ == "__main__":
    start_terminal_chat()
