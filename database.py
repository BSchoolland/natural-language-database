import sqlite3
import os

def create_connection():
    """Create a database connection to an SQLite database."""
    db_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Chinook_Sqlite.sqlite')
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)
    return None

def execute_query(conn, query):
    """Execute a single query."""
    cur = conn.cursor()
    try:
        cur.execute(query)
        conn.commit()
        if query.strip().upper().startswith('SELECT'):
            return cur.fetchall()
        else:
            return "Query executed successfully."
    except Exception as e:
        return str(e)
