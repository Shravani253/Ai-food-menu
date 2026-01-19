import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "Food_tranceability"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD"),
            port=int(os.getenv("DB_PORT", 5432)),
            cursor_factory=RealDictCursor
        )
        print("✅ PostgreSQL database connected successfully")
        return conn

    except psycopg2.Error as e:
        print("❌ Error while connecting to PostgreSQL")
        print(e)
        return None
if __name__ == "__main__":
    conn = get_db_connection()

    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT 1;")
            print("✅ Test query executed successfully")
            cur.close()
            conn.close()
        except Exception as e:
            print("❌ Query failed")
            print(e)
