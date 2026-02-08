import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from pathlib import Path

# Force-load .env from backend root
BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"

print("🔍 ENV PATH =", ENV_PATH)
print("🔍 ENV EXISTS =", ENV_PATH.exists())

load_dotenv(dotenv_path=ENV_PATH)

print("🔍 RAW ENV CONTENT:")
with open(ENV_PATH, "r") as f:
    print(f.read())

print("🔍 DB_NAME AFTER LOAD =", os.getenv("DB_NAME"))



def get_db_connection():
    """
    Create and return a PostgreSQL database connection.
    Returns None if connection fails.
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            dbname=os.getenv("DB_NAME", "ai_food_menu"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD"),
            port=int(os.getenv("DB_PORT", 5432)),
            cursor_factory=RealDictCursor,
        )

        # 🔑 IMPORTANT: enable autocommit BEFORE session-level commands
        conn.autocommit = True

        schema = os.getenv("DB_SCHEMA", "public")
        with conn.cursor() as cur:
            cur.execute(f"SET search_path TO {schema};")

        # 🔁 switch back to transactional mode if you want
        conn.autocommit = False

        return conn

    except psycopg2.Error as e:
        print("❌ PostgreSQL connection failed")
        print(e)
        return None


# ---------- Local test ----------
if __name__ == "__main__":
    conn = get_db_connection()

    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT current_schema();")
                print("✅ Connected to schema:", cur.fetchone()["current_schema"])
            conn.close()
        except Exception as e:
            print("❌ Database test query failed")
            print(e)
