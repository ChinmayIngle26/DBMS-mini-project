import streamlit as st
import sqlite3
import pandas as pd

# Database Connection Helper
@st.cache_resource
def get_db_connection():
    return sqlite3.connect("library.db", check_same_thread=False)

# Setup page configuration
st.set_page_config(
    page_title="Library Management System", 
    layout="wide", 
    page_icon="📚",
    initial_sidebar_state="expanded"
)

# Custom CSS for UI Improvements
st.markdown("""
    <style>
    /* Styling the main container */
    .main {
        background-color: #0E1117;
    }
    
    /* Sleek card design for metrics */
    div[data-testid="metric-container"] {
        background-color: #1E212B;
        border: 1px solid #333;
        padding: 5% 5% 5% 10%;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Headers with gradient */
    h1, h2, h3 {
        background: -webkit-linear-gradient(#f0b000, #ff4e00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Make tables wider and better spaced */
    .stDataFrame {
        border-radius: 10px !important;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# Helper function for getting temporary connections for transactions
def get_trx_connection():
    return sqlite3.connect("library.db", check_same_thread=False)

st.title("📚 Library Management Architecture")
st.markdown("A Modern Relational Database System")
st.divider()

# Navigation via Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3145/3145765.png", width=100)
    st.title("Navigation")
    page = st.radio(
        "",
        ["📊 Dashboard", "🔍 Search Catalog", "🔄 Issue & Return", "👤 User History", "💰 Fines & Payments"]
    )
    st.markdown("---")
    st.caption("DBMS Mini Project")
    st.caption("SQLite Backend Engine")

# ----------------- PAGE HANDLERS ----------------- #

if page == "📊 Dashboard":
    st.header("Library Analytics")
    try:
        conn = get_trx_connection()
        
        # Gathering metrics
        books_df = pd.read_sql_query("SELECT SUM(total_copies) as total, SUM(available_copies) as avail FROM Books", conn)
        active_issues_df = pd.read_sql_query("SELECT COUNT(*) as active_count FROM Issued_Books WHERE return_date IS NULL", conn)
        unpaid_fines_df = pd.read_sql_query("SELECT SUM(amount) as fine_sum FROM Fines WHERE paid_status = 0", conn)
        
        total_books = books_df.iloc[0]['total'] if not books_df.empty and pd.notna(books_df.iloc[0]['total']) else 0
        available_books = books_df.iloc[0]['avail'] if not books_df.empty and pd.notna(books_df.iloc[0]['avail']) else 0
        active_issues = active_issues_df.iloc[0]['active_count'] if not active_issues_df.empty and pd.notna(active_issues_df.iloc[0]['active_count']) else 0
        total_fines = unpaid_fines_df.iloc[0]['fine_sum'] if not unpaid_fines_df.empty and pd.notna(unpaid_fines_df.iloc[0]['fine_sum']) else 0
        conn.close()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Books", int(total_books))
        col2.metric("Available Stock", int(available_books), f"{int(available_books - total_books)} checked out")
        col3.metric("Active Borrows", int(active_issues))
        col4.metric("Pending Fines", f"₹ {total_fines:,.2f}")
        
    except Exception as e:
        st.error(f"Database Error: Could not load analytics. Backend offline? ({e})")

elif page == "🔍 Search Catalog":
    st.header("Search & View Books")
    
    search_term = st.text_input("🔍 Search by Title or Author", placeholder="Type 'Orwell' or '1984'...")
    
    try:
        conn = get_trx_connection()
        query = """
        SELECT book_id as "ID", title as "Book Title", author as "Author", 
               genre as "Genre", total_copies as "Total", available_copies as "Available"
        FROM Books
        WHERE title LIKE ? OR author LIKE ?
        ORDER BY book_id
        """
        df = pd.read_sql_query(query, conn, params=(f"%{search_term}%", f"%{search_term}%"))
        conn.close()
        
        if df.empty:
            st.info("No books found matching your criteria.")
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)
            
    except Exception as e:
        st.error(f"Database error: {e}")

elif page == "🔄 Issue & Return":
    st.header("Transaction Engine")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.subheader("📤 Issue Book")
        with st.form("issue_form"):
            member_id_issue = st.number_input("Member ID", min_value=1, step=1)
            book_id_issue = st.number_input("Book ID", min_value=1, step=1)
            issue_submitted = st.form_submit_button("Process Issue", use_container_width=True)
            
            if issue_submitted:
                conn = get_trx_connection()
                cur = conn.cursor()
                try:
                    # Manual availability check and issuance for SQLite without procedures
                    cur.execute("SELECT available_copies FROM Books WHERE book_id = ?", (book_id_issue,))
                    res = cur.fetchone()
                    if not res or res[0] <= 0:
                        raise Exception("Book is currently out of stock or does not exist")
                    
                    cur.execute("INSERT INTO Issued_Books (member_id, book_id, due_date) VALUES (?, ?, date('now', '+14 days'))", (member_id_issue, book_id_issue))
                    conn.commit()
                    st.success("✅ Book successfully checked out! Trigger automatically decreased stock.")
                    st.balloons()
                except Exception as e:
                    conn.rollback()
                    st.error(f"❌ Issuance Failed: {str(e).split('CONTEXT')[0]}")
                finally:
                    cur.close()
                    conn.close()

    with col2:
        st.subheader("📥 Return Book")
        with st.form("return_form"):
            issue_id_return = st.number_input("Issue ID (Transaction Ref)", min_value=1, step=1)
            return_submitted = st.form_submit_button("Process Return", use_container_width=True)
            
            if return_submitted:
                conn = get_trx_connection()
                cur = conn.cursor()
                try:
                    cur.execute("UPDATE Issued_Books SET return_date = date('now') WHERE issue_id = ?", (issue_id_return,))
                    if cur.rowcount > 0:
                        conn.commit()
                        st.success("✅ Return accepted! Trigger automatically replenished stock.")
                    else:
                        st.warning("⚠️ Invalid Issue ID. Transaction not found.")
                except Exception as e:
                    conn.rollback()
                    st.error(f"❌ Return Error: {str(e)}")
                finally:
                    cur.close()
                    conn.close()

elif page == "👤 User History":
    st.header("Member Timeline")
    
    member_id = st.number_input("Enter Member ID to query history:", min_value=1, step=1)
    
    if st.button("Fetch Ledger", type="primary"):
        try:
            conn = get_trx_connection()
            query = """
            SELECT ib.issue_id as "Issue ID", b.title as "Book", b.author as "Author", 
                   ib.issue_date as "Borrowed On", ib.due_date as "Due By", 
                   COALESCE(ib.return_date, 'ACTIVE') as "Returned On"
            FROM Issued_Books ib
            JOIN Books b ON ib.book_id = b.book_id
            WHERE ib.member_id = ?
            ORDER BY ib.issue_date DESC
            """
            df = pd.read_sql_query(query, conn, params=(member_id,))
            conn.close()
            
            if df.empty:
                st.info("Member ledger is currently empty.")
            else:
                st.dataframe(df, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"Database error: {e}")

elif page == "💰 Fines & Payments":
    st.header("Financial Compliance")
    
    try:
        conn = get_trx_connection()
        query = """
        SELECT f.fine_id as "Fine Ref", m.name as "Member Name", b.title as "Book Subject", 
               f.amount as "Amount Pending (₹)", f.paid_status as "Cleared"
        FROM Fines f
        JOIN Issued_Books ib ON f.issue_id = ib.issue_id
        JOIN Members m ON ib.member_id = m.member_id
        JOIN Books b ON ib.book_id = b.book_id
        WHERE f.paid_status = 0
        """
        df = pd.read_sql_query(query, conn)
        
        if df.empty:
            st.success("No active fines! Everyone is compliant. 🎉")
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.divider()
            st.subheader("Process Payment")
            col1, col2 = st.columns([1, 2])
            with col1:
                fine_id_pay = st.number_input("Enter Fine Ref to Clear:", min_value=1, step=1)
                clear_submit = st.button("Mark as Cleared", type="primary")
            with col2:
                if clear_submit:
                    cur = conn.cursor()
                    try:
                        cur.execute("UPDATE Fines SET paid_status = 1 WHERE fine_id = ?", (fine_id_pay,))
                        if cur.rowcount > 0:
                            conn.commit()
                            st.success("Payment Received and cleared! 💸")
                            st.rerun()
                        else:
                            st.warning("Fine ID does not exist or was already previously cleared.")
                    except Exception as e:
                        conn.rollback()
                        st.error(f"Database Error: {str(e)}")
                    finally:
                        cur.close()
        
        conn.close()
    except Exception as e:
        st.error(f"Database error: {e}")
