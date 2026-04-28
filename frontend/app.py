import streamlit as st
import sqlite3
import pandas as pd
import re

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

# Initialize theme in session state
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

# Define theme variables
if st.session_state.theme == "Dark":
    main_bg = "#0E1117"
    card_bg = "#1E212B"
    card_border = "#333"
    text_gradient = "-webkit-linear-gradient(#f0b000, #ff4e00)"
else:
    main_bg = "#ffffff"
    card_bg = "#f8f9fa"
    card_border = "#e0e0e0"
    text_gradient = "-webkit-linear-gradient(#1A2980, #26D0CE)"

# Custom CSS for UI Improvements
st.markdown(f"""
    <style>
    /* Styling the main container */
    .main {{
        background-color: {main_bg};
    }}
    
    /* Sleek card design for metrics */
    div[data-testid="metric-container"] {{
        background-color: {card_bg};
        border: 1px solid {card_border};
        padding: 5% 5% 5% 10%;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }}
    
    /* Headers with gradient */
    h1, h2, h3 {{
        background: {text_gradient};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    
    /* Make tables wider and better spaced */
    .stDataFrame {{
        border-radius: 10px !important;
        overflow: hidden;
    }}
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
    
    # Theme Selector
    selected_theme = st.radio("UI Theme", ["Dark", "Light"], index=0 if st.session_state.theme == "Dark" else 1, horizontal=True)
    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        st.rerun()

    page = st.radio(
        "",
        ["📊 Dashboard", "📚 Manage Books", "👥 Manage Users", "🔄 Issue & Return", "👤 User History", "💰 Fines & Payments"]
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

elif page == "📚 Manage Books":
    st.header("Book Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Search", "📖 Add", "✏️ Edit", "🗑️ Delete"])
    
    with tab1:
        search_term = st.text_input("🔍 Search by Title or Author", placeholder="Type 'Orwell' or '1984'...", key="search_book")
        
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
            
    with tab2:
        with st.form("add_book_form"):
            title = st.text_input("Title")
            author = st.text_input("Author")
            genre = st.text_input("Genre")
            total_copies = st.number_input("Total Copies", min_value=1, step=1)
            
            submitted = st.form_submit_button("Add Book", use_container_width=True)
            if submitted:
                if title and author:
                    try:
                        conn = get_trx_connection()
                        cur = conn.cursor()
                        cur.execute(
                            "INSERT INTO Books (title, author, genre, total_copies, available_copies) VALUES (?, ?, ?, ?, ?)",
                            (title, author, genre, total_copies, total_copies)
                        )
                        conn.commit()
                        st.success(f"✅ Successfully added '{title}' by {author}!")
                    except Exception as e:
                        conn.rollback()
                        st.error(f"❌ Failed to add book: {e}")
                    finally:
                        conn.close()
                else:
                    st.warning("Please fill in both Title and Author.")

    with tab3:
        st.subheader("Edit Existing Book")
        book_id_edit = st.number_input("Enter Book ID to Edit", min_value=1, step=1, key="edit_book_id")
        
        if st.button("Fetch Details", key="fetch_edit"):
            conn = get_trx_connection()
            cur = conn.cursor()
            cur.execute("SELECT title, author, genre, total_copies FROM Books WHERE book_id = ?", (book_id_edit,))
            book = cur.fetchone()
            conn.close()
            
            if book:
                st.session_state.edit_book_data = book
                st.session_state.edit_book_id = book_id_edit
            else:
                st.error("Book ID not found.")
                
        if 'edit_book_data' in st.session_state and st.session_state.get('edit_book_id') == book_id_edit:
            book = st.session_state.edit_book_data
            with st.form("edit_book_form"):
                new_title = st.text_input("Title", value=book[0])
                new_author = st.text_input("Author", value=book[1])
                new_genre = st.text_input("Genre", value=book[2])
                new_total = st.number_input("Total Copies", min_value=1, step=1, value=book[3])
                
                edit_submitted = st.form_submit_button("Update Book", use_container_width=True)
                if edit_submitted:
                    try:
                        conn = get_trx_connection()
                        cur = conn.cursor()
                        diff = new_total - book[3]
                        cur.execute(
                            "UPDATE Books SET title = ?, author = ?, genre = ?, total_copies = ?, available_copies = available_copies + ? WHERE book_id = ?",
                            (new_title, new_author, new_genre, new_total, diff, book_id_edit)
                        )
                        conn.commit()
                        st.success("✅ Book updated successfully!")
                        del st.session_state.edit_book_data
                        del st.session_state.edit_book_id
                    except Exception as e:
                        conn.rollback()
                        st.error(f"❌ Update failed: {e}")
                    finally:
                        conn.close()
                        
    with tab4:
        st.subheader("Delete a Book")
        book_id_del = st.number_input("Enter Book ID to Delete", min_value=1, step=1, key="del_book_id")
        st.warning("⚠️ Deleting a book will also remove its entire issue history.")
        if st.button("Delete Book", type="primary"):
            try:
                conn = get_trx_connection()
                cur = conn.cursor()
                cur.execute("DELETE FROM Books WHERE book_id = ?", (book_id_del,))
                if cur.rowcount > 0:
                    conn.commit()
                    st.success("✅ Book deleted successfully!")
                else:
                    st.error("Book ID not found.")
            except Exception as e:
                conn.rollback()
                st.error(f"❌ Deletion failed: {e}")
            finally:
                conn.close()

elif page == "👥 Manage Users":
    st.header("Member Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Search", "📖 Add", "✏️ Edit", "🗑️ Delete"])
    
    with tab1:
        search_term = st.text_input("🔍 Search by Name or Email", placeholder="Type name or email...", key="search_user")
        
        try:
            conn = get_trx_connection()
            query = """
            SELECT member_id as "ID", name as "Name", email as "Email", 
                   phone as "Phone", join_date as "Join Date"
            FROM Members
            WHERE name LIKE ? OR email LIKE ?
            ORDER BY member_id
            """
            df = pd.read_sql_query(query, conn, params=(f"%{search_term}%", f"%{search_term}%"))
            conn.close()
            
            if df.empty:
                st.info("No members found matching your criteria.")
            else:
                st.dataframe(df, use_container_width=True, hide_index=True)
                
        except Exception as e:
            st.error(f"Database error: {e}")

    with tab2:
        with st.form("add_user_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            phone = st.text_input("Phone Number")
            
            submitted = st.form_submit_button("Register Member", use_container_width=True)
            if submitted:
                if not name or not email:
                    st.warning("Please fill in both Name and Email.")
                elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    st.warning("Please enter a valid email address.")
                elif phone and not re.match(r"^\+?[\d\s\-]{10,15}$", phone):
                    st.warning("Please enter a valid phone number (10-15 digits).")
                else:
                    try:
                        conn = get_trx_connection()
                        cur = conn.cursor()
                        cur.execute(
                            "INSERT INTO Members (name, email, phone) VALUES (?, ?, ?)",
                            (name, email, phone)
                        )
                        conn.commit()
                        st.success(f"✅ Successfully registered member '{name}'!")
                    except sqlite3.IntegrityError:
                        conn.rollback()
                        st.error("❌ Email address is already registered.")
                    except Exception as e:
                        conn.rollback()
                        st.error(f"❌ Failed to register member: {e}")
                    finally:
                        conn.close()

    with tab3:
        st.subheader("Edit Existing Member")
        user_id_edit = st.number_input("Enter Member ID to Edit", min_value=1, step=1, key="edit_user_id")
        
        if st.button("Fetch Details", key="fetch_edit_user"):
            conn = get_trx_connection()
            cur = conn.cursor()
            cur.execute("SELECT name, email, phone FROM Members WHERE member_id = ?", (user_id_edit,))
            user = cur.fetchone()
            conn.close()
            
            if user:
                st.session_state.edit_user_data = user
                st.session_state.edit_user_id = user_id_edit
            else:
                st.error("Member ID not found.")
                
        if 'edit_user_data' in st.session_state and st.session_state.get('edit_user_id') == user_id_edit:
            user = st.session_state.edit_user_data
            with st.form("edit_user_form"):
                new_name = st.text_input("Full Name", value=user[0])
                new_email = st.text_input("Email Address", value=user[1])
                new_phone = st.text_input("Phone Number", value=user[2] if user[2] else "")
                
                edit_submitted = st.form_submit_button("Update Member", use_container_width=True)
                if edit_submitted:
                    if not new_name or not new_email:
                        st.warning("Please fill in both Name and Email.")
                    elif not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
                        st.warning("Please enter a valid email address.")
                    elif new_phone and not re.match(r"^\+?[\d\s\-]{10,15}$", new_phone):
                        st.warning("Please enter a valid phone number (10-15 digits).")
                    else:
                        try:
                            conn = get_trx_connection()
                            cur = conn.cursor()
                            cur.execute(
                                "UPDATE Members SET name = ?, email = ?, phone = ? WHERE member_id = ?",
                                (new_name, new_email, new_phone, user_id_edit)
                            )
                            conn.commit()
                            st.success("✅ Member updated successfully!")
                            del st.session_state.edit_user_data
                            del st.session_state.edit_user_id
                        except sqlite3.IntegrityError:
                            conn.rollback()
                            st.error("❌ Email address is already registered to another member.")
                        except Exception as e:
                            conn.rollback()
                            st.error(f"❌ Update failed: {e}")
                        finally:
                            conn.close()
                            
    with tab4:
        st.subheader("Delete a Member")
        user_id_del = st.number_input("Enter Member ID to Delete", min_value=1, step=1, key="del_user_id")
        st.warning("⚠️ Deleting a member will also remove their entire issue history and fines.")
        if st.button("Delete Member", type="primary", key="del_user_btn"):
            try:
                conn = get_trx_connection()
                cur = conn.cursor()
                cur.execute("DELETE FROM Members WHERE member_id = ?", (user_id_del,))
                if cur.rowcount > 0:
                    conn.commit()
                    st.success("✅ Member deleted successfully!")
                else:
                    st.error("Member ID not found.")
            except Exception as e:
                conn.rollback()
                st.error(f"❌ Deletion failed: {e}")
            finally:
                conn.close()

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
