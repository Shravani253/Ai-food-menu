class RestaurantTableRegistry:
    """
    Controls which tables restaurant staff are allowed to access.
    Staff can record events and manage menu data,
    but cannot directly manipulate system-derived fields.
    """

    ALLOWED_TABLES = {
        # Core entities
        "restaurant",
        "ingredients",
        "menu_items",
        "menu_ingredients",

        # Event & logging (append-only)
        "ingredient_events",

        # Optional / system-facing (read-only if enforced elsewhere)
        "storage_conditions",
    }

    @classmethod
    def validate_table(cls, table_name: str):
        if table_name not in cls.ALLOWED_TABLES:
            raise ValueError(f"Unauthorized table access: {table_name}")

