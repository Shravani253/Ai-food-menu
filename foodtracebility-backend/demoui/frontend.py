import streamlit as st
from io import BytesIO
from llm.llm_function import safe_rag_query

from database.qr_generator import generator_qr_for_dishes
from llm.llm_function import safe_rag_query
from llm.alerts_embeddings import generate_visual_alerts
visuals, dashboard = generate_visual_alerts(all_knowledge)

# ----------------------
# App State
# ----------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "dish_id" not in st.session_state:
    st.session_state.dish_id = None
if "ingredient" not in st.session_state:
    st.session_state.ingredient = None


# ----------------------
# Home Page
# ----------------------
if st.session_state.page == "home":
    st.title("🍕 Food Traceability System")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📱 Scanner for Consumers (Domino's)"):
            st.session_state.page = "consumer"

    with col2:
        if st.button("🏭 Login as Supplier"):
            st.session_state.page = "supplier"


# ----------------------
# Consumer Page (QR Scan Simulation)
# ----------------------
elif st.session_state.page == "consumer":
    st.title("📱 Consumer Scanner Mode")

    dish_id = st.text_input("Enter Dish ID (simulate QR scan):")

    if dish_id:
        st.session_state.dish_id = dish_id
        st.session_state.page = "dish"


# ----------------------
# Supplier Page (QR Generator)
# ----------------------
elif st.session_state.page == "supplier":
    st.title("🏭 Supplier Dashboard – QR Generator")

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


# ----------------------
# Dish → Ingredients Page
# ----------------------
elif st.session_state.page == "dish":
    st.title(f"🍽 Dish {st.session_state.dish_id} Ingredients")

    # Simulated fetch (you later connect to DB)
    dish_ingredients = {
        1: ["Pizza Base", "Mozzarella Cheese", "Tomato Sauce"],
        2: ["Pizza Base", "Cheese", "Capsicum", "Onion"],
        3: ["Pizza Base", "Paneer", "Capsicum"],
        4: ["Pizza Base", "Chicken Sausage", "Cheese"]
    }

    ingredients = dish_ingredients.get(int(st.session_state.dish_id), [])

    for ing in ingredients:
        if st.button(f"🧪 Know your {ing}"):
            st.session_state.ingredient = ing
            st.session_state.page = "chatbot"


# ----------------------
# Ingredient Chatbot
# ----------------------
elif st.session_state.page == "chatbot":
    st.title(f"🤖 Know Your {st.session_state.ingredient}")

    user_query = st.text_input(f"Ask about {st.session_state.ingredient}:")

    if st.button("Ask"):
        query = f"Give freshness, safety and risk analysis for ingredient {st.session_state.ingredient}"
        response = safe_rag_query(query)
        st.write(response)

    if st.button("⬅ Back to Ingredients"):
        st.session_state.page = "dish"

