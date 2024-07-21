import sqlite3

def setup(table_name='papers'):
    # Connect to the database (creates a new database if it doesn't exist)
    conn = sqlite3.connect('science_papers.db')
    c = conn.cursor()
    
    # Create a tables
    c.execute(f'''
    CREATE TABLE {table_name} (
            id INTEGER PRIMARY KEY,
            title TEXT,
            summary TEXT,
            author TEXT,
            year INTEGER,
            category TEXT,
            embedding BLOB
        )
    ''')

    c.execute('''
        CREATE TABLE "references" (
            parent_id INTEGER,
            child_id INTEGER,
            PRIMARY KEY (parent_id, child_id),
            FOREIGN KEY (parent_id) REFERENCES papers(id),
            FOREIGN KEY (child_id) REFERENCES papers(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Call the setup function
setup()
