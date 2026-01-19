import json
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, "food_ingredients.json")

print("Saving JSON to:", OUTPUT_FILE)

LAST_SYNC_FILE = os.path.join(BASE_DIR, "last_sync.txt")

# Read last sync time
if os.path.exists(LAST_SYNC_FILE):
    with open(LAST_SYNC_FILE, "r") as f:
        last_sync = f.read().strip()
else:
    last_sync = "1970-01-01 00:00:00"

# Safety check
if not last_sync:
    last_sync = "1970-01-01 00:00:00"

print("Last sync:", last_sync)

tables = {
    "vendors": "created_at",
    "ingredients": "created_at",
    "intake_events": "intake_datetime",
    "storage_details": "start_time",
    "transport_details": "dispatch_time",
    "outlets": "created_at",
    "distribution_details": "distributed_at",
    "quality_details": "checked_at",
    "dishes": "created_at",
    "dish_ingredients": None  # No timestamp, so full dump always
}

def get_new_rows(table, time_col):
    if time_col:
        query = f"""
        SELECT * FROM {table}
        WHERE {time_col} > :last_sync
        """
        with engine.connect() as conn:
            result = conn.execute(text(query), {"last_sync": last_sync})
            rows = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, r)) for r in rows]
    else:
        # If no timestamp column, fallback to full table
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM {table}"))
            rows = result.fetchall()
            columns = result.keys()
            return [dict(zip(columns, r)) for r in rows]


# Load existing JSON
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        existing_data = json.load(f)
else:
    existing_data = {table: [] for table in tables.keys()}

new_data_found = False

for table, time_col in tables.items():
    new_rows = get_new_rows(table, time_col)
    if new_rows:
        existing_data[table].extend(new_rows)
        new_data_found = True
        print(f"{len(new_rows)} new rows added to {table}")

# Save updated JSON
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(existing_data, f, indent=4, default=str)

print("JSON successfully written.")


# Update last sync time
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(LAST_SYNC_FILE, "w") as f:
    f.write(now)

print("Sync completed at:", now)
