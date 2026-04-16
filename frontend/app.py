import streamlit as st
import psycopg2
import pandas as pd

# Database Connection Helper
def get_connection():
    # Will try to connect with default user and localhost
    return psycopg2.connect(dbname="library_db")

st.set_page_config(page_title="Library Management System", layout="wide", page_icon="📚")

st.title("📚 Library Management System")

# Navigation
page = st.sidebar.selectbox(
    "Navigation",
    ["Search Books", "Issue / Return Book", "Member History", "Fine Status"]
)

if page == "Search Books":
    st.header("Search & View Books")
    
    search_term = st.text_input("Enter Book Title or Author")
    
    try:
        conn = get_connection()
        query = """
        SELECT book_id, title, author, genre, total_copies, available_copies
        FROM Books
        WHERE title ILIKE %s OR author ILIKE %s
        ORDER BY book_id
        """
        df = pd.read_sql_query(query, conn, params=(f"%{search_term}%", f"%{search_term}%"))
        conn.close()
        
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Database error: {e}")

elif page == "Issue / Return Book":
    st.header("Issue or Return a Book")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Issue Book")
        member_id_issue = st.number_input("Member ID", min_value=1, step=1, key="issue_mem")
        book_id_issue = st.number_input("Book ID", min_value=1, step=1, key="issue_book")
        
        if st.button("Issue Book"):
            conn = get_connection()
            cur = conn.cursor()
            try:
                # Call stored procedure
                cur.execute("CALL procedure_issue_book(%s, %s)", (member_id_issue, book_id_issue))
                conn.commit()
                st.success("Book issued successfully! The trigger automatically updated the available copies.")
            except Exception as e:
                conn.rollback()
                st.error(f"Error issuing book: {str(e)}")
            finally:
                cur.close()
                conn.close()

    with col2:
        st.subheader("Return Book")
        issue_id_return = st.number_input("Issue ID", min_value=1, step=1, key="ret_issue")
        
        if st.button("Return Book"):
            conn = get_connection()
            cur = conn.cursor()
            try:
                # Update return date
                cur.execute("UPDATE Issued_Books SET return_date = CURRENT_DATE WHERE issue_id = %s", (issue_id_return,))
                if cur.rowcount > 0:
                    conn.commit()
                    st.success("Book returned successfully! The trigger automatically updated the available copies.")
                else:
                    st.warning("Issue ID not found.")
            except Exception as e:
                conn.rollback()
                st.error(f"Error returning book: {str(e)}")
            finally:
                cur.close()
                conn.close()

elif page == "Member History":
    st.header("Member History")
    
    member_id = st.number_input("Enter Member ID", min_value=1, step=1)
    
    if st.button("View History"):
        try:
            conn = get_connection()
            query = """
            SELECT ib.issue_id, b.title, b.author, ib.issue_date, ib.due_date, ib.return_date
            FROM Issued_Books ib
            JOIN Books b ON ib.book_id = b.book_id
            WHERE ib.member_id = %s
            ORDER BY ib.issue_date DESC
            """
            df = pd.read_sql_query(query, conn, params=(member_id,))
            conn.close()
            
            if df.empty:
                st.info("No borrowing history found for this member.")
            else:
                st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Database error: {e}")

elif page == "Fine Status":
    st.header("Unpaid Fines")
    
    try:
        conn = get_connection()
        query = """
        SELECT f.fine_id, m.name as Member_Name, b.title as Book_Title, f.amount, f.paid_status
        FROM Fines f
        JOIN Issued_Books ib ON f.issue_id = ib.issue_id
        JOIN Members m ON ib.member_id = m.member_id
        JOIN Books b ON ib.book_id = b.book_id
        WHERE f.paid_status = FALSE
        """
        df = pd.read_sql_query(query, conn)
        
        st.dataframe(df, use_container_width=True)
        
        st.subheader("Pay Fine")
        fine_id_pay = st.number_input("Enter Fine ID to Mark as Paid", min_value=1, step=1)
        if st.button("Mark Paid"):
            cur = conn.cursor()
            try:
                cur.execute("UPDATE Fines SET paid_status = TRUE WHERE fine_id = %s", (fine_id_pay,))
                if cur.rowcount > 0:
                    conn.commit()
                    st.success("Fine marked as paid!")
                    st.rerun()
                else:
                    st.warning("Fine ID not found or already paid.")
            except Exception as e:
                conn.rollback()
                st.error(f"Error: {str(e)}")
            finally:
                cur.close()
                conn.close()
    except Exception as e:
        st.error(f"Database error: {e}")
