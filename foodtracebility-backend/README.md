Food Traceability Backend (PostgreSQL + QR + RAG)

This repository contains the backend logic for a food traceability system that enables end-to-end visibility of ingredients used in prepared dishes.

The system allows suppliers, warehouses, and outlets to log supply-chain events, generate QR codes for dishes, and convert structured trace data into human-readable food stories using RAG + LLM.

📌 Backend Responsibilities
Store supply-chain data in PostgreSQL
Allow dynamic data entry across multiple tables
Generate QR codes for dishes
Fetch and join traceability data
Convert raw data into readable explanations for customers

🗂️ Backend Folder Structure
backend/
│
├── app.py

├── database_sql.py

├── interactive_populate.py

├── schema.sql

├── config.py

└── requirements.txt

🧠 Database Tables Used

The backend operates on the following tables:

vendors

ingredients

intake_events

storage_details

transport_details

outlets

distribution_details

quality_details

dishes

dish_ingredients

All tables are connected via foreign keys to enable full traceability.

⚙️ File Responsibilities

1️⃣ app.py — Application Orchestrator

Acts as the entry point for the backend.

Responsibilities:

Accepts input for data insertion
Allows selection of target table
Dynamically fetches table schema
Routes data to the database layer
Triggers QR generation when dishes are created
Acts as the interface for QR-based trace requests

2️⃣ database_sql.py — Database & QR Engine

Handles all database interactions and QR generation.
Database responsibilities:
Connect to PostgreSQL
Fetch table schemas dynamically
Insert rows into any supported table
Execute join queries for dish traceability

QR responsibilities:

Generate QR codes for dishes
Encode trace URLs instead of raw data
Store QR images locally or serve via API

Typical QR payload:

/trace?dish_id=<dish_id>

3️⃣ interactive_populate.py — RAG + LLM Layer

Transforms structured trace data into human-readable explanations.

Responsibilities:

Fetch trace data for a dish
Pull quality and storage information
Calculate freshness and lifespan
Build RAG context from database output
Generate customer-friendly food descriptions using an LLM

Example Output:

The dish you are eating was prepared using fresh ingredients
that passed quality checks today and were stored under
optimal temperature conditions.

🔁 Backend Workflow
Data Entry
→ app.py
→ database_sql.py
→ PostgreSQL

Dish Creation
→ QR Generated

QR Scan
→ app.py
→ database_sql.py (joins)
→ interactive_populate.py (RAG + LLM)
→ Readable food trace output

🧪 Quality & Freshness Logic

Quality data is fetched from quality_details
Storage conditions influence freshness evaluation
Shelf-life is calculated programmatically
LLM output is grounded in database data, not hallucinated

🧾 SQL Schema

All database tables and constraints are defined in:

schema.sql


The schema includes:

Primary keys
Foreign keys
Indexes for performance
Timestamp tracking

🔐 Design Principles

Database-first traceability
No hard-coded schemas
Separation of concerns
LLM used only for interpretation

QR as an access layer, not storage
