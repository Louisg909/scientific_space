import sqlite3
import traceback

class db:
    def __init__(self, argument):
        self.file = 'science_papers.db'
        self.conn = None
        self.c = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.c = self.conn.cursor()
        self._create_tables()  # Ensure tables are created
        return self

    def __exit__(self, exc_type, exc_value, traceback_obj):
        if exc_type is None:
            self.conn.commit()
        else:
            traceback.print_exception(exc_type, exc_value, traceback_obj)
        if self.conn is not None:
            self.conn.close()

    def _create_tables(self):
        """Create tables if they do not exist."""
        table_creation_queries = [
            '''
            CREATE TABLE IF NOT EXISTS papers (
                id INTEGER PRIMARY KEY,
                title TEXT,
                summary TEXT,
                author TEXT,
                year INTEGER,
                category TEXT,
                embedding BLOB
            )
            ''',
            '''
            CREATE TABLE IF NOT EXISTS citation_papers (
                id INTEGER PRIMARY KEY,
                title TEXT,
                summary TEXT,
                author TEXT,
                year INTEGER,
                category TEXT,
                embedding BLOB,
                cited_by INTEGER,
                cites INTEGER,
                contribution_vector BLOB,
                contribution_magnitude FLOAT
            )
            ''',
            '''
            CREATE TABLE IF NOT EXISTS references (
                parent_id INTEGER,
                child_id INTEGER,
                weighting FLOAT,
                PRIMARY KEY (parent_id, child_id),
                FOREIGN KEY (parent_id) REFERENCES papers(id),
                FOREIGN KEY (child_id) REFERENCES papers(id)
            )
            '''
        ]
        
        for query in table_creation_queries:
            self.c.execute(query)

def insert(self, table, columns, row):
    """
    Inserts data into the specified table in the SQLite database.
    
    Args:
        table (str): The name of the table where data will be inserted.
        columns (list of str): The list of column names for the table.
        row (tuple): A tuple representing a single row of data. The order should match the `columns` list.
    
    Returns:
        int: The ID of the inserted or existing record.
    """
    # Create placeholders for the SQL queries
    placeholders = ', '.join('?' for _ in columns)
    
    # Build the SELECT query to check if the row already exists
    check_query = f'''
        SELECT id FROM {table}
        WHERE {' AND '.join([f"{col} = ?" for col in columns])}
    '''
    self.c.execute(check_query, row)
    existing_id = self.c.fetchone()
    
    if existing_id:
        # If it exists, return the existing ID
        return existing_id[0]
    else:
        # Build the INSERT query
        insert_query = f'''
            INSERT INTO {table} ({', '.join(columns)})
            VALUES ({placeholders})
        '''
        self.c.execute(insert_query, row)
        # Get the ID of the newly inserted record
        return self.c.lastrowid


    def access(self, table='papers', select='*', limit=None):
        """
        Accesses the specified table in the SQLite database and yields rows one at a time.
    
        Args:
            table (str): The name of the table to query. Defaults to 'papers'.
            select (str): The columns to select from the table. Defaults to '*', which selects all columns.
            limit (int, optional): The maximum number of rows to return. If None, all rows are returned.
    
        Yields:
            tuple: A tuple representing a row in the result set.
        """
        query = f'SELECT {select} FROM {table}'
        if limit is not None:
            query += f' LIMIT {limit}'
        
        self.c.execute(query)
    
        while True:
            row = self.c.fetchone()
            if row is None:
                break
            yield row

    def grab(self, table='papers', select='*', where=None):
        """
        Fetches a single row based on the specified conditions.
    
        Args:
            table (str): The name of the table to query.
            select (str): The columns to select.
            where (tuple): A tuple where the first element is a list of column names for conditions,
                            and the second element is a tuple of values for these conditions.
    
        Returns:
            tuple: A tuple representing a row in the result set or None if no row matches.
        """
        query = f'SELECT {select} FROM {table}'
        if where:
            query += ' WHERE ' + ' AND '.join([f"{column} = ?" for column in where[0]])
        
        query += ' LIMIT 1'
    
        self.c.execute(query, where[1] if where else ())
        return self.c.fetchone()

    def edit(self, table, function, condition=None):
        """
        Processes all rows in the specified table and updates them based on a function.
    
        Args:
            table (str): The name of the table to be edited.
            function (func): The function that takes an old row and returns a new row.
            condition (str, optional): The condition to filter rows. It should be a valid SQL condition.
        """
        query = f'SELECT * FROM {table}'
        if condition:
            query += f' WHERE {condition}'
        
        self.c.execute(query)
        rows = self.c.fetchall()
    
        column_names = [description[0] for description in self.c.description]
    
        for row in rows:
            new_row = function(row)
    
            set_clause = ', '.join(f"{col} = ?" for col in column_names[1:])
    
            self.c.execute(f'''
                UPDATE {table}
                SET {set_clause}
                WHERE {column_names[0]} = ?
            ''', new_row[1:] + (row[0],))

    def show_tables(self):
        """
        Returns a list of all table names in the SQLite database.
    
        Returns:
            list: A list of table names.
        """
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.c.fetchall()
        return [table[0] for table in tables]



