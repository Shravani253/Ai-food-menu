from app.services.postgres import get_db_connection
from app.services.restaurant_table import RestaurantTableRegistry


class RestaurantDBService:
    """
    Handles all database metadata operations for restaurant staff.
    """

    @staticmethod
    def fetch_all_tables(only_allowed: bool = True):
        """
        Fetch all tables present in the connected PostgreSQL database.

        :param only_allowed: If True, return only tables allowed by RestaurantTableRegistry
        :return: List of table names
        """

        conn = get_db_connection()
        if conn is None:
            raise RuntimeError("Database connection not available")

        try:
            cur = conn.cursor()

            query = """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                  AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """

            cur.execute(query)
            db_tables = [row["table_name"] for row in cur.fetchall()]

            if only_allowed:
                return sorted(
                    RestaurantTableRegistry.ALLOWED_TABLES.intersection(db_tables)
                )

            return db_tables

        except Exception as e:
            raise RuntimeError("Failed to fetch tables from database") from e

        finally:
            cur.close()
            conn.close()

    @staticmethod
    def fetch_rows(table_name: str, limit: int = 50):
        """
        Fetch rows from a selected table (validated).
        """

        RestaurantTableRegistry.validate_table(table_name)

        conn = get_db_connection()
        if not conn:
            raise RuntimeError("Database connection not available")

        try:
            cur = conn.cursor()

            query = f"""
                SELECT *
                FROM {table_name}
                LIMIT %s;
            """

            cur.execute(query, (limit,))
            return cur.fetchall()

        finally:
            cur.close()
            conn.close()

    @staticmethod
    def insert_row(table_name: str, data: dict):
        """
        Insert a row into a selected table (validated).
        """

        RestaurantTableRegistry.validate_table(table_name)

        if not data:
            raise ValueError("No data provided for insert")

        conn = get_db_connection()
        if not conn:
            raise RuntimeError("Database connection not available")

        try:
            cur = conn.cursor()

            columns = ", ".join(data.keys())
            placeholders = ", ".join(["%s"] * len(data))
            values = tuple(data.values())

            query = f"""
                INSERT INTO {table_name} ({columns})
                VALUES ({placeholders})
                RETURNING *;
            """

            cur.execute(query, values)
            inserted_row = cur.fetchone()
            conn.commit()

            return inserted_row

        finally:
            cur.close()
            conn.close()
