-- 1. Books currently issued by a member (e.g., member_id = 1)
SELECT b.title, b.author, ib.issue_date, ib.due_date 
FROM Issued_Books ib
JOIN Books b ON ib.book_id = b.book_id
WHERE ib.member_id = 1 AND ib.return_date IS NULL;

-- 2. Overdue books with member details
SELECT m.name, m.email, b.title, ib.due_date, CURRENT_DATE - ib.due_date AS days_overdue
FROM Issued_Books ib
JOIN Members m ON ib.member_id = m.member_id
JOIN Books b ON ib.book_id = b.book_id
WHERE ib.return_date IS NULL AND ib.due_date < CURRENT_DATE;

-- 3. Most borrowed books
SELECT b.title, COUNT(ib.book_id) as borrow_count
FROM Issued_Books ib
JOIN Books b ON ib.book_id = b.book_id
GROUP BY b.book_id, b.title
ORDER BY borrow_count DESC
LIMIT 5;

-- 4. Members with unpaid fines
SELECT m.name, f.amount, b.title
FROM Fines f
JOIN Issued_Books ib ON f.issue_id = ib.issue_id
JOIN Members m ON ib.member_id = m.member_id
JOIN Books b ON ib.book_id = b.book_id
WHERE f.paid_status = FALSE;

-- 5. Available copies of a book by title (e.g., '1984')
SELECT title, total_copies, available_copies
FROM Books
WHERE title ILIKE '%1984%';
