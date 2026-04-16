# 📚 Library Management System - DBMS Mini Project

A comprehensive Library Management System backend built heavily upon **PostgreSQL** showcasing constraints, normalization, and advanced *PL/pgSQL* procedural logic. It encapsulates its capability with a modern sleek frontend constructed using **Python** & **Streamlit**.

## ✨ Features
- **ACID Compliant Database**: Normalized architecture strictly enforcing referential integrity.
- **Automated Inventory Tracking**: Relies on Database Triggers (`trg_update_copies`) to maintain accurate live-inventory whenever a checkout/return happens instead of trusting external applications.
- **Robust Exception Handling**: Stored Procedures (`procedure_issue_book`) validate stock dynamically via logical sequences prior to row insertion. 
- **Analytical Ledger Viewing**: Rich queries that aggregate transaction behaviors and monitor fines effortlessly.
- **Sleek Aesthetic Frontend**: Modern interactive interface equipped with dark-modes, grid layouts, and active metric dashboards.

---

## 🛠️ Technology Stack
- **RDBMS Engine**: PostgreSQL (Targeting v12+)
- **Scripting Environment**: Standard SQL, PL/pgSQL
- **Frontend App**: Python 3, Streamlit
- **Communication Protocol**: `psycopg2-binary`, `pandas`

---

## 🚀 Setup & Execution 

### 1: Postgres Environment
Ensure `PostgreSQL` is natively installed and running locally.
```bash
# Using Homebrew on macOS
brew services start postgresql
```

### 2: Constructing the Backend
Execute the raw scripts against the local PostgreSQL engine sequence:
```bash
createdb library_db
psql -d library_db -f db_scripts/schema.sql
psql -d library_db -f db_scripts/plsql_blocks.sql
psql -d library_db -f db_scripts/dummy_data.sql
```

### 3: Initializing the UI Engine
Spin up the `Streamlit` app inside a virtual environment for best parity.
```bash
# Ensure you are at the project root
python3 -m venv venv
source venv/bin/activate
pip install -r frontend/requirements.txt

# Run the app locally (Defaults to port 8501)
streamlit run frontend/app.py
```

---

## 🏗️ PL/SQL Implementations Documented
This framework rigorously checks the functional requirements via:
- **Trigger** -> Auto-updates `available_copies` across `Books` upon `Issued_Books` insertions/updates.
- **Procedure** -> Encases the book issue workflows.
- **Function** -> Calculates active numeric fine penalty values mathematically natively within Postgres.
- **Cursors** -> Employs efficient line-by-line reporting functionality for ledger processing.

## 📝 Deliverables Provided
- Complete architecture detailed in `docs/Report.md`.
- Mathematical relational mapping showcased at `docs/ER_Diagram.md`.
