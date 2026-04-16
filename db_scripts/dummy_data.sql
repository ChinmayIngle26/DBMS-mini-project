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

-- Note: We will use the stored procedure or insert statements to issue books, 
-- which will naturally test the Trigger!

-- Issuing books directly (trg_update_copies will fire)
INSERT INTO Issued_Books (member_id, book_id, issue_date, due_date) VALUES
(1, 1, CURRENT_DATE - INTERVAL '20 days', CURRENT_DATE - INTERVAL '6 days'), -- Overdue
(2, 2, CURRENT_DATE - INTERVAL '5 days', CURRENT_DATE + INTERVAL '9 days'),
(3, 5, CURRENT_DATE - INTERVAL '2 days', CURRENT_DATE + INTERVAL '12 days'),
(1, 4, CURRENT_DATE - INTERVAL '15 days', CURRENT_DATE - INTERVAL '1 day'); -- Overdue

-- Returning a book manually to test trigger
UPDATE Issued_Books SET return_date = CURRENT_DATE WHERE issue_id = 2;

-- Generating Fines for the overdue books (Issue 1 and 4)
-- We will use the calculate_fine function we created
INSERT INTO Fines (issue_id, amount) VALUES
(1, calculate_fine(1)),
(4, calculate_fine(4));
