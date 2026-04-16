-- PL/SQL Blocks (PL/pgSQL for PostgreSQL)

-- 1. Trigger Function: Auto-update available_copies in Books when issued or returned
CREATE OR REPLACE FUNCTION trg_update_copies()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        -- Book is issued, decrease available_copies
        UPDATE Books
        SET available_copies = available_copies - 1
        WHERE book_id = NEW.book_id;
    ELSIF TG_OP = 'UPDATE' AND OLD.return_date IS NULL AND NEW.return_date IS NOT NULL THEN
        -- Book is returned, increase available_copies
        UPDATE Books
        SET available_copies = available_copies + 1
        WHERE book_id = NEW.book_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 1a. The Trigger attaching the function to Issued_Books
DROP TRIGGER IF EXISTS trg_issue_return_book ON Issued_Books;
CREATE TRIGGER trg_issue_return_book
AFTER INSERT OR UPDATE OF return_date ON Issued_Books
FOR EACH ROW
EXECUTE FUNCTION trg_update_copies();

-- 2. Procedure: Issue a book
CREATE OR REPLACE PROCEDURE procedure_issue_book(p_member_id INT, p_book_id INT)
LANGUAGE plpgsql AS $$
DECLARE
    v_available_copies INT;
BEGIN
    -- Check availability
    SELECT available_copies INTO v_available_copies
    FROM Books WHERE book_id = p_book_id;

    IF v_available_copies <= 0 THEN
        RAISE EXCEPTION 'Book is currently out of stock';
    END IF;

    -- Insert record into Issued_Books (Trigger will auto-update the copies)
    INSERT INTO Issued_Books (member_id, book_id, due_date)
    VALUES (p_member_id, p_book_id, CURRENT_DATE + INTERVAL '14 days');
    
END;
$$;

-- 3. Function: Calculate fine amount
CREATE OR REPLACE FUNCTION calculate_fine(p_issue_id INT)
RETURNS NUMERIC AS $$
DECLARE
    v_due_date DATE;
    v_return_date DATE;
    v_fine_amount NUMERIC := 0;
    v_days_overdue INT;
BEGIN
    SELECT due_date, COALESCE(return_date, CURRENT_DATE) 
    INTO v_due_date, v_return_date
    FROM Issued_Books WHERE issue_id = p_issue_id;

    IF v_return_date > v_due_date THEN
        v_days_overdue := v_return_date - v_due_date;
        v_fine_amount := v_days_overdue * 2.00; -- ₹2/day
    END IF;

    RETURN v_fine_amount;
END;
$$ LANGUAGE plpgsql;

-- 4. Cursor for reporting currently issued books
CREATE OR REPLACE FUNCTION report_issued_books()
RETURNS TABLE (
    p_issue_id INT,
    p_member_name VARCHAR,
    p_book_title VARCHAR,
    p_issue_date DATE,
    p_due_date DATE
) AS $$
DECLARE
    issue_cursor CURSOR FOR
        SELECT ib.issue_id, m.name, b.title, ib.issue_date, ib.due_date
        FROM Issued_Books ib
        JOIN Members m ON ib.member_id = m.member_id
        JOIN Books b ON ib.book_id = b.book_id
        WHERE ib.return_date IS NULL;
    record_row RECORD;
BEGIN
    FOR record_row IN issue_cursor LOOP
        p_issue_id := record_row.issue_id;
        p_member_name := record_row.name;
        p_book_title := record_row.title;
        p_issue_date := record_row.issue_date;
        p_due_date := record_row.due_date;
        RETURN NEXT;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
