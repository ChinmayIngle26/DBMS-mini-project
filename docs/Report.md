# Library Management System - DBMS Mini Project Report

## 1. Project Overview
The "Library Management System" (LMS) is a modernized relational database project designed to streamline the operations of a library. The goal of this mini-project is to showcase the efficient utilization of Relational Database Management Systems (RDBMS) via Data Definition Language (DDL), Data Manipulation Language (DML), standard SQL triggers, and interactive application constraints. We utilized a lightweight SQLite database to run the backend natively without heavy procedural servers. Finally, a graphical user interface (GUI) was developed using Python and Streamlit to interact dynamically with the database.

## 2. Database Design & Schema
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

## 3. SQL Requirements and Implementation

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

## 4. Triggers and Application Logic
The implementation leverages standard SQL functionality embedded natively inside the fast SQLite engine alongside python logic.

1. **Trigger Engine (`trg_issue_book_update_copies`)**: 
   An automated database trigger attached to the `Issued_Books` table on `INSERT` and `UPDATE`. When a book is issued, it dynamically decrements the `available_copies`. When a book is returned (i.e., `return_date` flips from `NULL`), it inherently increments the `available_copies`.
2. **Application Constraints (Transaction Safe)**:
   Encapsulates the transactional logic safely inside Python `app.py`. It explicitly checks the `available_copies` logic securely inside standard queries, raising an algorithmic exception if stock is depleted, preventing standard triggers from failing negative checks. 
3. **Native Analytics Arithmetic**:
   Determines dynamic system properties directly computing intervals using `date('now', '+14 days')` during execution runs.

## 5. Frontend UI
A minimalistic UI was architected utilizing **Python** combined with **Streamlit** and heavily reliant on the `sqlite3` library to facilitate DB integration smoothly.
- The user can view global library catalogs and search gracefully.
- The interaction interface executes direct transactional payloads across protected UI endpoints.
- Error handling catches database exceptions dynamically and relays them securely to the frontend, preventing system outages.

### Tech Stack Utilized
- **Engine**: SQLite 3 (Lightweight RDBMS Engine)
- **Frontend**: Python 3 / Streamlit
- **Communication Protocol**: `sqlite3` interface, `pandas` standardizing datasets.

## 6. Conclusion
The LMS effectively simulates enterprise software by bridging normalized relational mappings with strict constraint enforcement and programmatic logic loops embedded in web routes securely avoiding procedural PL/pgSQL network bottlenecks locally!
