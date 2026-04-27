# 📚 Library Management System - DBMS Mini Project

A comprehensive Library Management System backend built heavily upon **SQLite** showcasing constraints, normalization, and standard SQL triggers. It encapsulates its capability with a modern sleek frontend constructed using **Python** & **Streamlit**.

## ✨ Features
- **ACID Compliant Database**: Normalized architecture strictly enforcing referential integrity.
- **Automated Inventory Tracking**: Relies on Database Triggers (`trg_issue_book_update_copies`) to maintain accurate live-inventory whenever a checkout/return happens instead of trusting external applications.
- **Robust Application Logic**: Application-layer checks validate stock dynamically prior to row insertion, allowing standard SQL triggers to enforce consistency safely. 
- **Analytical Ledger Viewing**: Rich SQL queries that aggregate transaction behaviors and monitor fines effortlessly natively using parameter interpolation for security.
- **Sleek Aesthetic Frontend**: Modern interactive interface equipped with dark-modes, grid layouts, and active metric dashboards.

---

## 🛠️ Technology Stack
- **RDBMS Engine**: SQLite (Embedded Database `.db` file system)
- **Scripting Environment**: Standard pure SQL
- **Frontend App**: Python 3, Streamlit
- **Communication Protocol**: `sqlite3`, `pandas`

---

## 🚀 Setup & Execution 

### 1: Initializing the Database Environment
We use a lightweight Python script to compile the schema structure and inject the dummy data into a local `library.db` artifact automatically.
```bash
python3 init_db.py
```

### 2: Booting the Application UI
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

## 🏗️ Technical Implementations Documented
This framework rigorously checks the functional requirements via standard paradigms without requiring heavy procedural servers:
- **Triggers** -> Executes automatically inside SQLite to increment/decrement `available_copies` on the `Books` mapping directly reacting to `Issued_Books`.
- **Primary & Foreign Keys** -> Ensures relationships between Active Checkouts and Fines strictly resolve towards Active Members.
- **Application Validation** -> Validates constraints interactively via cursor logic within python instead of custom un-portable PL/pgSQL procedures.

## 📝 Deliverables Provided
- Complete architecture detailed in `docs/Report.md`.
- Mathematical relational mapping showcased at `docs/ER_Diagram.md`.
