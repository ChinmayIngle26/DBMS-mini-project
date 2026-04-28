# Library Management System - DBMS Mini Project Report

## Problem Statement
Traditional library systems often struggle with inefficient tracking of physical inventory, manual penalty calculations for overdue items, and a lack of real-time consistency between book availability and active checkouts. The objective of this project is to architect a reliable, digital Library Management System (LMS) capable of autonomously managing circulation, enforcing strict data constraints, and ensuring transaction safety through an automated database backend.

## 1. Project Overview
The "Library Management System" (LMS) is a modernized relational database project designed to streamline the operations of a library. The goal of this mini-project is to showcase the efficient utilization of Relational Database Management Systems (RDBMS) via Data Definition Language (DDL), Data Manipulation Language (DML), standard SQL triggers, and interactive application constraints. We utilized a lightweight SQLite database to run the backend natively without heavy procedural servers. Finally, a graphical user interface (GUI) was developed using Python and Streamlit to interact dynamically with the database.

## 2. Project Architecture
The architecture of the Library Management System is built upon a 2-tier internal model encapsulating the user interaction and localized database processing securely within the workspace:

- **Frontend/Presentation**: The graphical user interface (GUI) is generated dynamically via **Streamlit**. It processes user interaction payloads and provides comprehensive data visualization tables and active metrics.
- **Application Logic**: The middleware layer, driven by **Python**, handles the communication bridge. It validates stock constraints dynamically avoiding hard database faults, and constructs prepared SQL statements mapping python data structures into relational paradigms using Pandas.
- **Database Backend**: Grounded around a locally managed **SQLite** state file (`library.db`). The RDBMS ensures robust ACID compliance natively, maintaining referential integrity across the graph and deploying pure SQL standard Triggers to execute automatic adjustments independently. 

## 3. Project Structure
The repository is segmented into independent environments isolating database mapping, analytical logic, and presentation workflows:

```text
DBMS-mini-project/
├── db_scripts/
│   ├── schema.sql         # Base database schema, constraints, and Triggers
│   ├── dummy_data.sql     # Data payloads to test functionality visually
│   └── queries.sql        # Analytics query extracts
├── docs/
│   ├── ER_Diagram.md      # Visual entity relational map
│   └── Report.md          # Project analysis
├── frontend/
│   ├── app.py             # Streamlit graphical UI & middleware logic
│   └── requirements.txt   # Interface dependency manifest
├── init_db.py             # Python script initializing the `.db` ecosystem
└── README.md              # Setup instructions
```

## 4. Database Design & Schema
The database (`library.db`) is normalized and specifically crafted using 4 core tables:

### 2.1 Core Entities and Attributes
- **Members**: Tracks registered library members.
  - `member_id` (Primary Key), `name`, `email` (Unique), `phone`, `join_date`
- **Books**: The inventory of the library. 
  - `book_id` (Primary Key), `title`, `author`, `genre`, `total_copies` (CHECK >= 0), `available_copies` (CHECK >= 0 AND <= total_copies)
- **Issued_Books**: The transactional junction tracking borrowed books.
  - `issue_id` (Primary Key), `member_id` (Foreign Key - cascade delete), `book_id` (Foreign Key - cascade delete), `issue_date`, `due_date`, `return_date`.
- **Fines**: Handles penalty tracking for overdue books.
  - `fine_id` (Primary Key), `issue_id` (Foreign Key), `amount`, `paid_status` (INTEGER boolean logic 0/1).

*Refer to the attached `ER_Diagram.md` for the visual entity-relationship structure.*

## 5. SQL Requirements and Implementation

### 3.1 DDL & DML
The SQL scripts enforce vital database constraints:
- `PRIMARY KEY AUTOINCREMENT` to maintain tuple uniqueness natively.
- `FOREIGN KEY` cascades to prevent orphaned records.
- `NOT NULL` for crucial metadata such as `name` and `due_date`.
- `CHECK` constraints on `Books` (e.g., `available_copies <= total_copies`) and `Issued_Books` (e.g., `due_date >= issue_date`).

### 3.2 Meaningful Queries Developed
At least 5 business-critical SQL structures are supplied dynamically:
1. **Current Issues**: Finds active borrowings using `return_date IS NULL`.
2. **Overdue Books**: Compares `date('now')` against `due_date` utilizing table joins.
3. **Most Borrowed Analytics**: Aggregates datasets grouping transaction behavior metrics efficiently.
4. **Unpaid Fines**: Filters by boolean logical flags (`paid_status = 0`).
5. **Book Availability**: Implements pattern matching (`LIKE`) to search subsets.

## 6. Triggers and Application Logic
The implementation leverages standard SQL functionality embedded natively inside the fast SQLite engine alongside python logic.

1. **Trigger Engine (`trg_issue_book_update_copies`)**: 
   An automated database trigger attached to the `Issued_Books` table on `INSERT` and `UPDATE`. When a book is issued, it dynamically decrements the `available_copies`. When a book is returned (i.e., `return_date` flips from `NULL`), it inherently increments the `available_copies`.
2. **Application Constraints (Transaction Safe)**:
   Encapsulates the transactional logic safely inside Python `app.py`. It explicitly checks the `available_copies` logic securely inside standard queries, raising an algorithmic exception if stock is depleted, preventing standard triggers from failing negative checks. 
3. **Native Analytics Arithmetic**:
   Determines dynamic system properties directly computing intervals using `date('now', '+14 days')` during execution runs.

## 7. Frontend UI
A minimalistic UI was architected utilizing **Python** combined with **Streamlit** and heavily reliant on the `sqlite3` library to facilitate DB integration smoothly.
- The user can view global library catalogs and search gracefully.
- The interaction interface executes direct transactional payloads across protected UI endpoints.
- Error handling catches database exceptions dynamically and relays them securely to the frontend, preventing system outages.

### Tech Stack Utilized
- **Engine**: SQLite 3 (Lightweight RDBMS Engine)
- **Frontend**: Python 3 / Streamlit
- **Communication Protocol**: `sqlite3` interface, `pandas` standardizing datasets.

## 8. Conclusion
The LMS effectively simulates enterprise software by bridging normalized relational mappings with strict constraint enforcement and programmatic logic loops embedded in web routes securely avoiding procedural PL/pgSQL network bottlenecks locally!
