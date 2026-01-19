import os
import qrcode
from io import BytesIO
from PIL import Image
import json

# ===============================
# Config
# ===============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QR_OUTPUT_DIR = os.path.join(BASE_DIR, "qr_codes")
JSON_PATH = os.path.join(BASE_DIR, "database", "food_ingredients.json")

STREAMLIT_BASE_URL = "http://localhost:8501"   # production: https://yourdomain.com

os.makedirs(QR_OUTPUT_DIR, exist_ok=True)


# ===============================
# Load dishes from JSON
# ===============================

def load_dishes():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["dishes"]


# ===============================
# Generate QR for each dish
# ===============================

def generate_qr_for_dishes():
    dishes = load_dishes()

    print("📦 Generating QR codes for dishes...\n")

    for dish in dishes:
        dish_id = dish["dish_id"]
        dish_name = dish["dish_name"]

        # URL that QR will contain
        qr_url = f"{STREAMLIT_BASE_URL}/?dish_id={dish_id}"

        # Create QR
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=8,
            border=4,
        )
        qr.add_data(qr_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Save file
        filename = f"dish_{dish_id}_{dish_name.replace(' ', '_')}.png"
        filepath = os.path.join(QR_OUTPUT_DIR, filename)
        img.save(filepath)

        print(f"✅ {dish_name}")
        print(f"   Dish ID : {dish_id}")
        print(f"   QR URL  : {qr_url}")
        print(f"   Saved   : {filepath}\n")

    print("🔥 All QR codes generated successfully.")
    print(f"📂 Location: {QR_OUTPUT_DIR}")


# ===============================
# Run from terminal
# ===============================

if __name__ == "__main__":
    generate_qr_for_dishes()
