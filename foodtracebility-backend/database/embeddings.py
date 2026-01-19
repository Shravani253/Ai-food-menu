import json
import os
from datetime import datetime

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


# =========================
# Utils
# =========================

def parse_datetime(dt: str) -> datetime:
    return datetime.strptime(dt, "%Y-%m-%d %H:%M:%S.%f")


def calculate_days(start, end):
    return max((end - start).total_seconds() / 86400, 0)


# =========================
# Freshness Logic
# =========================

def calculate_freshness(ingredient, intake, storage, transport, outlet):
    created_at = parse_datetime(ingredient["created_at"])
    intake_time = parse_datetime(intake["intake_datetime"])

    storage_start = parse_datetime(storage["start_time"])
    storage_end = parse_datetime(storage["end_time"])

    dispatch = parse_datetime(transport["dispatch_time"])
    arrival = parse_datetime(transport["arrival_time"])

    outlet_time = parse_datetime(outlet["created_at"])

    waiting_days = calculate_days(created_at, intake_time)
    storage_days = calculate_days(storage_start, storage_end)
    transport_days = calculate_days(dispatch, arrival)
    outlet_delay_days = calculate_days(arrival, outlet_time)

    total_days = waiting_days + storage_days + transport_days + outlet_delay_days
    life_span = intake["life_span_days"]

    status = "Fresh" if total_days <= life_span else "Expired"

    return {
        "waiting_days": round(waiting_days, 2),
        "storage_days": round(storage_days, 2),
        "transport_days": round(transport_days, 2),
        "outlet_delay_days": round(outlet_delay_days, 2),
        "total_days": round(total_days, 2),
        "life_span": life_span,
        "status": status
    }


# =========================
# Quantity Logic
# =========================

def calculate_quantity(ingredient_id, intake, dishes, dish_ingredients):
    intake_qty = float(intake["quantity"])
    total_used = 0.0

    for di in dish_ingredients:
        if di["ingredient_id"] == ingredient_id:
            dish = next(d for d in dishes if d["dish_id"] == di["dish_id"])
            total_used += dish["total_sold"] * float(di["quantity_used"])

    remaining = intake_qty - total_used
    status = "Valid" if remaining >= 0 else "Overused"

    return {
        "intake": intake_qty,
        "used": round(total_used, 2),
        "remaining": round(remaining, 2),
        "status": status
    }


# =========================
# Knowledge Builder
# =========================

def build_ingredient_knowledge(
    ingredient,
    intake,
    storage,
    transport,
    outlet,
    dishes,
    dish_ingredients
):
    freshness = calculate_freshness(
        ingredient, intake, storage, transport, outlet
    )

    quantity = calculate_quantity(
        ingredient["ingredient_id"],
        intake,
        dishes,
        dish_ingredients
    )

    alerts = []
    if freshness["status"] == "Expired":
        alerts.append("Ingredient expired by freshness rules")
    if quantity["status"] != "Valid":
        alerts.append("Ingredient quantity overused")

    return {
        "ingredient_id": ingredient["ingredient_id"],
        "name": ingredient["ingredient_name"],
        "freshness": freshness,
        "quantity": quantity,
        "alerts": alerts
    }


def knowledge_to_text(k):
    return f"""
Ingredient: {k['name']} (ID {k['ingredient_id']})

Freshness:
- Status: {k['freshness']['status']}
- Total Days: {k['freshness']['total_days']}
- Allowed Lifespan: {k['freshness']['life_span']} days

Quantity:
- Intake: {k['quantity']['intake']}
- Used: {k['quantity']['used']}
- Remaining: {k['quantity']['remaining']}
- Status: {k['quantity']['status']}

Alerts:
{', '.join(k['alerts']) if k['alerts'] else 'No risks detected'}
""".strip()


# =========================
# Main
# =========================

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    JSON_PATH = os.path.join(BASE_DIR, "food_ingredients.json")

    print("Using JSON:", JSON_PATH)

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("✔ Loaded JSON snapshot\n")

    # Build indexes (SQL-like joins)
    intake_index = {i["ingredient_id"]: i for i in data["intake_events"]}
    storage_index = {s["intake_id"]: s for s in data["storage_details"]}
    transport_index = {t["intake_id"]: t for t in data["transport_details"]}

    outlet = data["outlets"][0]  # Only one outlet in your JSON

    # Init embedding infra once
    model = SentenceTransformer("all-MiniLM-L6-v2")

    chroma_client = chromadb.Client(
        Settings(
            persist_directory=os.path.join(BASE_DIR, "chroma_db"),
            anonymized_telemetry=False
        )
    )

    collection = chroma_client.get_or_create_collection(
        name="food_traceability_embeddings"
    )

    for ingredient in data["ingredients"]:
        ing_id = ingredient["ingredient_id"]

        if ing_id not in intake_index:
            print(f"⚠ No intake event for ingredient {ing_id}, skipping")
            continue

        intake = intake_index[ing_id]
        storage = storage_index.get(intake["intake_id"])
        transport = transport_index.get(intake["intake_id"])

        if not storage or not transport:
            print(f"⚠ Missing storage or transport for ingredient {ing_id}, skipping")
            continue

        knowledge = build_ingredient_knowledge(
            ingredient,
            intake,
            storage,
            transport,
            outlet,
            data["dishes"],
            data["dish_ingredients"]
        )

        print(json.dumps(knowledge, indent=4))

        document = knowledge_to_text(knowledge)

        embeddings = model.encode([document])

        collection.add(
            documents=[document],
            embeddings=embeddings.tolist(),
            metadatas=[{
                "ingredient_id": knowledge["ingredient_id"],
                "name": knowledge["name"]
            }],
            ids=[f"ingredient_{knowledge['ingredient_id']}"]
        )

        print(f"✅ Embedded: {knowledge['name']}")

    print("\n🔥 Pipeline complete: JSON → Intelligence → Embeddings → ChromaDB")
