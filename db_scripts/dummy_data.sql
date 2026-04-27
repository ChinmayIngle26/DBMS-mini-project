-- Insert Members
INSERT INTO Members (name, email, phone) VALUES
('Alice Smith', 'alice@example.com', '1234567890'),
('Bob Johnson', 'bob@example.com', '0987654321'),
('Charlie Brown', 'charlie@example.com', '1122334455'),
('Diana Prince', 'diana@example.com', '5566778899');

-- Insert Books
INSERT INTO Books (title, author, genre, total_copies, available_copies) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 5, 5),
('1984', 'George Orwell', 'Dystopian', 3, 3),
('To Kill a Mockingbird', 'Harper Lee', 'Fiction', 4, 4),
('Brief Answers to the Big Questions', 'Stephen Hawking', 'Science', 2, 2),
('Atomic Habits', 'James Clear', 'Self-help', 10, 10);

-- Issuing books directly (trg_issue_book_update_copies will fire)
INSERT INTO Issued_Books (member_id, book_id, issue_date, due_date) VALUES
(1, 1, date('now', '-20 days'), date('now', '-6 days')), -- issue_id 1 (Overdue)
(2, 2, date('now', '-5 days'), date('now', '+9 days')),  -- issue_id 2
(3, 5, date('now', '-2 days'), date('now', '+12 days')), -- issue_id 3
(1, 4, date('now', '-15 days'), date('now', '-1 day'));  -- issue_id 4 (Overdue)

-- Returning a book manually to test trigger
UPDATE Issued_Books SET return_date = date('now') WHERE issue_id = 2;

-- Generating Fines for the overdue books (Issue 1 and 4) manually for dummy data
-- In SQLite we calculate the fine amount statically for dummy data
INSERT INTO Fines (issue_id, amount) VALUES
(1, 12.00), -- 6 days overdue at ₹2/day
(4, 2.00);  -- 1 day overdue at ₹2/day
