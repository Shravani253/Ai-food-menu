from app.services.postgres import get_db_connection
from app.services.supplier_table import SupplierTableRegistry


class SupplierDBService:
    """
    Handles all database metadata operations for suppliers
    """

    @staticmethod
    def fetch_all_tables(only_allowed: bool = True):
        """
        Fetch all tables present in the connected PostgreSQL database.

        :param only_allowed: If True, return only tables allowed by SupplierTableRegistry
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

            # Because you are using RealDictCursor
            db_tables = [row["table_name"] for row in cur.fetchall()]

            # Optional filtering using registry
            if only_allowed:
                return sorted(
                    SupplierTableRegistry.ALLOWED_TABLES.intersection(db_tables)
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
        Fetch rows from a selected table
        """

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
            rows = cur.fetchall()

            return rows

        finally:
            cur.close()
            conn.close()

    @staticmethod
    def insert_row(table_name: str, data: dict):
        """
        Insert a row into a selected table
        """

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

if __name__ == "__main__":
    service = SupplierDBService()

    print("\n📦 Fetching available tables...\n")
    tables = service.fetch_all_tables(only_allowed=False)

    if not tables:
        print("❌ No tables found")
        exit()

    for i, table in enumerate(tables, start=1):
        print(f"{i}. {table}")

    choice = int(input("\n👉 Select a table number: "))
    table_name = tables[choice - 1]

    print(f"\n📄 Fetching rows from '{table_name}'...\n")
    rows = service.fetch_rows(table_name, limit=10)

    if not rows:
        print("⚠️ No rows found")
    else:
        for row in rows:
            print(row)

    insert = input("\n➕ Do you want to insert a new row? (y/n): ").lower()

    if insert == "y":
        print("\n📝 Enter column=value (type 'done' to finish):")

        data = {}
        while True:
            entry = input("> ")
            if entry.lower() == "done":
                break
            if "=" not in entry:
                print("❌ Invalid format. Use column=value")
                continue

            key, value = entry.split("=", 1)
            data[key.strip()] = value.strip()

        inserted_row = service.insert_row(table_name, data)

        print("\n✅ Row inserted successfully:")
        print(inserted_row)

    print("\n🎉 Done testing database operations\n")

