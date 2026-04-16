-- DDL for Database Schema with Constraints

-- Drop tables if they already exist (for clean setup)
DROP TABLE IF EXISTS Fines CASCADE;
DROP TABLE IF EXISTS Issued_Books CASCADE;
DROP TABLE IF EXISTS Books CASCADE;
DROP TABLE IF EXISTS Members CASCADE;

-- Create Members table
CREATE TABLE Members (
    member_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    join_date DATE DEFAULT CURRENT_DATE
);

-- Create Books table
CREATE TABLE Books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    genre VARCHAR(50),
    total_copies INT NOT NULL CHECK (total_copies >= 0),
    available_copies INT NOT NULL CHECK (available_copies >= 0 AND available_copies <= total_copies)
);

-- Create Issued_Books table
CREATE TABLE Issued_Books (
    issue_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES Members(member_id) ON DELETE CASCADE,
    book_id INT REFERENCES Books(book_id) ON DELETE CASCADE,
    issue_date DATE DEFAULT CURRENT_DATE,
    due_date DATE NOT NULL,
    return_date DATE,
    CHECK (due_date >= issue_date),
    CHECK (return_date IS NULL OR return_date >= issue_date)
);

-- Create Fines table
CREATE TABLE Fines (
    fine_id SERIAL PRIMARY KEY,
    issue_id INT REFERENCES Issued_Books(issue_id) ON DELETE CASCADE,
    amount NUMERIC(10, 2) NOT NULL CHECK (amount >= 0),
    paid_status BOOLEAN DEFAULT FALSE
);
