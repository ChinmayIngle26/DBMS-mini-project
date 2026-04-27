import sqlite3
import os

DB_FILE = "library.db"

def init_db():
    if os.path.exists(DB_FILE):
        print(f"Removing existing {DB_FILE}...")
        os.remove(DB_FILE)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        print("Executing schema.sql...")
        with open('db_scripts/schema.sql', 'r') as f:
            cursor.executescript(f.read())
            
        print("Executing dummy_data.sql...")
        with open('db_scripts/dummy_data.sql', 'r') as f:
            cursor.executescript(f.read())
            
        conn.commit()
        print(f"Database successfully initialized at {DB_FILE} ✅")
    except Exception as e:
        print(f"Error initializing DB: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
