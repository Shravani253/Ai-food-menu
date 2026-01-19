import streamlit as st
from io import BytesIO
import qrcode

from llm.llm_function import safe_rag_query, get_llm
from database.qr_generator import generate_qr_for_dishes
from llm.alerts_embeddings import generate_visual_alerts


# ======================
# Init (safe + clean)
# ======================

llm = get_llm()   # lazy + event-loop safe (as we designed earlier)


# ======================
# App State
# ======================

if "page" not in st.session_state:
    st.session_state.page = "home"
if "dish_id" not in st.session_state:
    st.session_state.dish_id = None
if "ingredient" not in st.session_state:
    st.session_state.ingredient = None


# ======================
# Home Page
# ======================

if st.session_state.page == "home":
    st.title("🍕 Food Traceability System")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📱 Scanner for Consumers (Domino's)"):
            st.session_state.page = "consumer"

    with col2:
        if st.button("🏭 Login as Supplier"):
            st.session_state.page = "supplier"


# ======================
# Consumer Page
# ======================

elif st.session_state.page == "consumer":
    st.title("📱 Consumer Scanner Mode")

    dish_id = st.text_input("Enter Dish ID (simulate QR scan):")

    if dish_id:
        st.session_state.dish_id = dish_id
        st.session_state.page = "dish"


# ======================
# Supplier Page
# ======================

elif st.session_state.page == "supplier":
    st.title("🏭 Supplier Dashboard – QR Generator")

    if st.button("Generate All Dish QR Codes"):
        generate_qr_for_dishes()
        st.success("All QR codes generated and saved successfully!")

    st.divider()

    dishes = {
        1: "Margherita",
        2: "Farmhouse",
        3: "Peppy Paneer",
        4: "Chicken Sausage Pizza"
    }

    for dish_id, name in dishes.items():
        st.subheader(f"{name} (Dish ID: {dish_id})")

        url = f"http://localhost:8501/?dish_id={dish_id}"

        qr = qrcode.make(url)
        buf = BytesIO()
        qr.save(buf)
        st.image(buf.getvalue(), width=150)
        st.caption(url)


# ======================
# Dish → Ingredients Page
# ======================

elif st.session_state.page == "dish":
    st.title(f"🍽 Dish {st.session_state.dish_id} Ingredients")

    dish_ingredients = {
        1: ["Pizza Base", "Mozzarella Cheese", "Tomato Sauce"],
        2: ["Pizza Base", "Cheese", "Capsicum", "Onion"],
        3: ["Pizza Base", "Paneer", "Capsicum"],
        4: ["Pizza Base", "Chicken Sausage", "Cheese"]
    }

    ingredients = dish_ingredients.get(int(st.session_state.dish_id), [])

    if not ingredients:
        st.warning("No ingredients found for this dish.")

    for ing in ingredients:
        if st.button(f"🧪 Know your {ing}"):
            st.session_state.ingredient = ing
            st.session_state.page = "chatbot"

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"


# ======================
# Ingredient Chatbot Page
# ======================

elif st.session_state.page == "chatbot":
    st.title(f"🤖 Know Your {st.session_state.ingredient}")

    user_query = st.text_input(f"Ask about {st.session_state.ingredient}:")

    if st.button("Ask"):
        query = (
            f"Give freshness, safety, storage condition, expiry risks and "
            f"health impact for ingredient {st.session_state.ingredient}"
        )
        with st.spinner("AI is analyzing..."):
            response = safe_rag_query(query)
            st.write(response)

    if st.button("⬅ Back to Ingredients"):
        st.session_state.page = "dish"
