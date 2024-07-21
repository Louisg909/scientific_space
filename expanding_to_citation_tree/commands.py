import sqlite3

def add_table(table_name='papers'):
    conn = sqlite3.connect('science_papers.db')
    c = conn.cursor()

    try:
        c.execute(f'''
            CREATE TABLE {table_name} (
                id INTEGER PRIMARY KEY,
                title TEXT,
                summary TEXT,
                author TEXT,
                year INTEGER,
                category TEXT,
                embedding BLOB
            );
            CREATE TABLE references (
                parent_id INTEGER,
                child_id INTEGER,
                PRIMARY KEY (parent_id, child_id),
                FOREIGN KEY (parent_id) REFERENCES papers(id),
                FOREIGN KEY (child_id) REFERENCES papers(id)
            );
        ''')
    except sqlite3.OperationalError as e:
        print(e)

    conn.commit()
    conn.close()


def insert(table='papers', *data:tuple):
    """
    Inserts data into the specified table in the SQLite database.

    Args:
        table (str): The name of the table where data will be inserted.
        data (tuple): Variable length argument list of tuples, where each tuple represents a row.
            Each tuple must have the following structure:
            (title, summary, author, year, category, embedding)
    """
    conn = sqlite3.connect('science_papers.db')
    c = conn.cursor()

    dupe_count = 0

    for row in data:
        title, summary, author, year, category, embedding = row
        
        # Check if the paper already exists
        c.execute(f'''
            SELECT 1 FROM {table}
            WHERE title = ? AND summary = ? AND year = ?
        ''', (title, summary, year))
        
        if not c.fetchone():
            # Insert the paper if it doesn't already exist
            c.execute(f'''
                INSERT INTO {table} (title, summary, author, year, category, embedding)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, summary, author, year, category, embedding))
        else:
            dupe_count += 1
    
    conn.commit()
    conn.close()

    print(f'Duplicate papers: {dupe_count}')


def access(table='papers', select='*', limit=None):
    """
    Accesses the specified table in the SQLite database and yields rows one at a time.

    Args:
        table (str): The name of the table to query. Defaults to 'papers'.
        select (str): The columns to select from the table. Defaults to '*', which selects all columns.
        limit (int, optional): The maximum number of rows to return. If None, all rows are returned.

    Yields:
        tuple: A tuple representing a row in the result set.

    Example:
        To fetch and print the first 10 rows from the 'papers' table:
        
        for row in access(select='title, summary', table='papers', limit=10):
            print(row)
    """
    conn = sqlite3.connect('science_papers.db')
    c = conn.cursor()

    query = f'SELECT {select} FROM {table}'
    if limit is not None:
        query += f' LIMIT {limit}'
    
    c.execute(query)

    try:
        while True:
            row = c.fetchone()
            if row is None:
                break
            yield row
    finally:
        conn.close()

def grab(table='papers', select='*', where=None):
    conn = sqlite3.connect('science_papers.db')
    c = conn.cursor()

    query = f'SELECT {select} FROM {table}'
    if where:
        query += ' WHERE ' + ' AND '.join([f"{column} = ?" for column in where[0]])

    query += ' LIMIT 1'

    c.execute(query, where[1])
    row = c.fetchone()
    conn.close()
    return row


def edit(table, function, condition=None):
    """
    Processes all rows in the specified table and updates the final column with the processed value.

    Args:
        table (str): The name of the table to be edited.
        function (func): The function that will take an input of the old tuple, and give an output of the new tuple.
        condition (str, optional): The condition to filter rows. It should be a valid SQL condition (e.g., "embedding = ?").

    Example usage:
        edit('your_table_name', processing_function, "embedding = 'b\"\"'")
    """
    conn = sqlite3.connect('science_papers.db')
    c = conn.cursor()

    # Build the SQL query
    query = f'SELECT * FROM {table}'
    if condition:
        query += f' WHERE {condition}'
    
    # Fetch all rows from the table with the given condition
    c.execute(query)
    rows = c.fetchall()

    # Get the column names
    column_names = [description[0] for description in c.description]

    for row in rows:
        new_row = function(row)

        # Build the SET clause for the UPDATE statement
        set_clause = ', '.join(f"{col} = ?" for col in column_names[1:])  # Skip the primary key column

        # Update the table with the processed row
        c.execute(f'''
            UPDATE {table}
            SET {set_clause}
            WHERE {column_names[0]} = ?
        ''', new_row[1:] + (row[0],))  # Skip the primary key in the new row and use it in the WHERE clause

    conn.commit()
    conn.close()


def show_tables():
    conn = sqlite3.connect('science_papers.db')
    c = conn.cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()

    conn.close()
    return [table[0] for table in tables]
