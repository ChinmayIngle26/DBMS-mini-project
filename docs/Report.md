# Library Management System - DBMS Mini Project Report

## 1. Project Overview
The "Library Management System" (LMS) is a modernized relatioanl database project designed to streamline the operations of a library. The goal of this mini-project is to showcase the efficient utilization of Relational Database Management Systems (RDBMS) via Data Definition Language (DDL), Data Manipulation Language (DML), advanced queries, and PL/SQL blocks (Procedural SQL - implemented via PL/pgSQL for PostgreSQL). Finally, a minimal graphical user interface (GUI) was developed using Python and Streamlit to interact dynamically with the database.

## 2. Database Design & Schema
The database (`library_db`) is normalized and specifically crafted using 4 core tables:

### 2.1 Core Entities and Attributes
- **Members**: Tracks registered library members.
  - `member_id` (Primary Key), `name`, `email` (Unique), `phone`, `join_date`
- **Books**: The inventory of the library. 
  - `book_id` (Primary Key), `title`, `author`, `genre`, `total_copies` (CHECK >= 0), `available_copies` (CHECK >= 0 AND <= total_copies)
- **Issued_Books**: The transactional junction tracking borrowed books.
  - `issue_id` (Primary Key), `member_id` (Foreign Key - cascade delete), `book_id` (Foreign Key - cascade delete), `issue_date`, `due_date`, `return_date`.
- **Fines**: Handles penalty tracking for overdue books.
  - `fine_id` (Primary Key), `issue_id` (Foreign Key), `amount`, `paid_status`.

*Refer to the attached `ER_Diagram.md` for the visual entity-relationship structure.*

## 3. SQL Requirements and Implementation

### 3.1 DDL & DML
The SQL scripts enforce vital database constraints:
- `PRIMARY KEY` to maintain tuple uniqueness.
- `FOREIGN KEY` cascades to prevent orphaned records.
- `NOT NULL` for crucial metadata such as `name` and `due_date`.
- `CHECK` constraints on `Books` (e.g., `available_copies <= total_copies`) and `Issued_Books` (e.g., `due_date >= issue_date`).

### 3.2 Meaningful Queries Developed
At least 5 business-critical SQL structures are supplied in `queries.sql`:
1. **Current Issues**: Finds active borrowings using `return_date IS NULL`.
2. **Overdue Books**: Compares `CURRENT_DATE` against `due_date` utilizing table joins.
3. **Most Borrowed**: Aggregates with `COUNT` and groups by book title.
4. **Unpaid Fines**: Filters by boolean logical flags (`paid_status = FALSE`).
5. **Book Availability**: Implements pattern matching (`ILIKE`) to search subsets.

## 4. PL/SQL Implementations
The implementation uses PostgreSQL's advanced PL/pgSQL language to strictly enforce business logic at the schema level.

1. **Trigger Engine (`trg_update_copies`)**: 
   An automated database trigger attached to the `Issued_Books` table on `INSERT` and `UPDATE`. When a book is issued, it dynamically decrements the `available_copies`. When a book is returned (i.e., `return_date` flips from `NULL`), it inherently increments the `available_copies`.
2. **Stored Procedure (`procedure_issue_book`)**:
   Encapsulates the transactional logic involved in issuing a book. It safely checks the `available_copies` using a `SELECT INTO` operation, throws an algorithmic EXCEPTION if out of stock, and if stock exists, it executes the insertion with a due date of `CURRENT_DATE + 14 days`.
3. **Functions (`calculate_fine`)**:
   Determines dynamical late-fee arithmetic, multiplying days overdue intrinsically by the ₹2/day baseline.
4. **Cursors (`report_issued_books`)**:
   Provides structured navigation iterating line-by-line via a CURSOR construct to output active borrows cleanly.

## 5. Frontend UI
A minimalistic UI was architected utilizing **Python** combined with **Streamlit** and heavily reliant on the `psycopg2-binary` library to facilitate DB integration.
- The user can view global library catalogs and search gracefully.
- The interaction interface executes direct DB calls (`CALL procedure_issue_book()`).
- Error handling catches database exceptions dynamically and relays them securely to the frontend, preventing system outages.

### Tech Stack Utilized
- **Engine**: PostgreSQL v14+
- **Frontend**: Python 3 / Streamlit
- **Visualization**: Markdown Mermaid

## 6. Conclusion
The LMS effectively simulates enterprise software by bridging normalized relational mappings with strict constraint enforcement and procedural logic components. Moving the complex calculations specifically into the engine via PL/pgSQL significantly reduces network load and assures absolute atomic consistency.
