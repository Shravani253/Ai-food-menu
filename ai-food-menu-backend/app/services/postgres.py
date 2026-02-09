import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Safe: loads .env locally if present, ignored on Render
load_dotenv()


def get_db_connection():
    """
    Create and return a PostgreSQL database connection.
    Works for both LOCAL (.env) and RENDER (environment variables).
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

        # Enable autocommit before session-level commands
        conn.autocommit = True

        schema = os.getenv("DB_SCHEMA", "public")
        with conn.cursor() as cur:
            cur.execute(f"SET search_path TO {schema};")

        # Optional: return to transactional mode
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
