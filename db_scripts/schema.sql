-- DDL for Database Schema with Constraints (SQLite version)

-- Drop tables if they already exist (for clean setup)
DROP TABLE IF EXISTS Fines;
DROP TABLE IF EXISTS Issued_Books;
DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Members;

-- Create Members table
CREATE TABLE Members (
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    join_date DATE DEFAULT (date('now'))
);

-- Create Books table
CREATE TABLE Books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    genre VARCHAR(50),
    total_copies INT NOT NULL CHECK (total_copies >= 0),
    available_copies INT NOT NULL CHECK (available_copies >= 0 AND available_copies <= total_copies)
);

-- Create Issued_Books table
CREATE TABLE Issued_Books (
    issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INT REFERENCES Members(member_id) ON DELETE CASCADE,
    book_id INT REFERENCES Books(book_id) ON DELETE CASCADE,
    issue_date DATE DEFAULT (date('now')),
    due_date DATE NOT NULL,
    return_date DATE,
    CHECK (due_date >= issue_date),
    CHECK (return_date IS NULL OR return_date >= issue_date)
);

-- Create Fines table
-- In SQLite, BOOLEAN is just an alias for integer (0 false, 1 true)
CREATE TABLE Fines (
    fine_id INTEGER PRIMARY KEY AUTOINCREMENT,
    issue_id INT REFERENCES Issued_Books(issue_id) ON DELETE CASCADE,
    amount NUMERIC(10, 2) NOT NULL CHECK (amount >= 0),
    paid_status INTEGER DEFAULT 0
);

-- Triggers to handle available_copies logic that used to be a PL/SQL Procedure/Trigger
CREATE TRIGGER trg_issue_book_update_copies
AFTER INSERT ON Issued_Books
BEGIN
    UPDATE Books
    SET available_copies = available_copies - 1
    WHERE book_id = NEW.book_id;
END;

CREATE TRIGGER trg_return_book_update_copies
AFTER UPDATE OF return_date ON Issued_Books
WHEN OLD.return_date IS NULL AND NEW.return_date IS NOT NULL
BEGIN
    UPDATE Books
    SET available_copies = available_copies + 1
    WHERE book_id = NEW.book_id;
END;
