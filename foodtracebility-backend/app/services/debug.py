from fastapi import FastAPI, Body, HTTPException
from app.services.supplier_db import SupplierDBService
import os

print("🔥🔥🔥 LOADED app/main.py 🔥🔥🔥")

app = FastAPI(
    title="Food Traceability Backend",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"status": "API is running"}

# 🔹 FETCH rows from a selected table
@app.get("/db/{table_name}/rows")
def get_table_rows(table_name: str, limit: int = 50):
    rows = SupplierDBService.fetch_rows(
        table_name=table_name,
        limit=limit
    )
    return {
        "table": table_name,
        "count": len(rows),
        "rows": rows
    }


# 🔹 INSERT data into a selected table
@app.post("/db/{table_name}/insert")
def insert_into_table(
    table_name: str,
    data: dict = Body(...)
):
    row = SupplierDBService.insert_row(
        table_name=table_name,
        data=data
    )
    return {
        "message": "Row inserted successfully",
        "table": table_name,
        "row": row
    }