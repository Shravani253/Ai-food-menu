class SupplierTableRegistry:
    """
    Controls which tables suppliers are allowed to access
    """

    ALLOWED_TABLES = {
        "vendor",
        "ingredients",
        "intake_events",
        "storage_details",
        "transport_details",
        "quality_details",
        "outlets",
        "distribution_details",
        "dish_ingredients",
        "dishes",
    }

    @classmethod
    def validate_table(cls, table_name: str):
        if table_name not in cls.ALLOWED_TABLES:
            raise ValueError(f"Unauthorized table access: {table_name}")
