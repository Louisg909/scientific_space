
import sqlite3
import traceback


class db:
    def __init__(self):
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
            CREATE TABLE IF NOT EXISTS paper_references (
                parent_id INTEGER,
                child_id INTEGER,
                weighting FLOAT,
                PRIMARY KEY (parent_id, child_id),
                FOREIGN KEY (parent_id) REFERENCES papers(id),
                FOREIGN KEY (child_id) REFERENCES papers(id)
            )
            ''',
            '''
            CREATE TABLE IF NOT EXISTS author_papers (
                id INTEGER PRIMARY KEY,
                title TEXT,
                summary TEXT,
                year INTEGER,
                author_id INTEGER,
                embedding BLOB,
                FOREIGN KEY (author_id) REFERENCES authors(id)
            )
            ''',
            '''
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY,
                name TEXT
                )
            '''
        ]
        
        for query in table_creation_queries:
            self.c.execute(query)

    def _tuple_to_dict(self, row, table='papers'):
        from .embed_data import translate
        if table == 'citation_papers':
            return {}
        elif table == 'paper_references': # idk when this would be used, but might as well throw it in now for ease.
            return {}
        return {'id': row[0], 'title': row[1], 'summary': row[2], 'author': row[3], 'year': row[4], 'category': row[5], 'embedding': translate(row[6])}

    def _dict_to_tuple(dictionary):
        return


    def _get_columns_for_table(self, table):
        """
        Fetches the column names for the specified table from the SQLite database.
        
        Args:
            table (str): The name of the table.
        
        Returns:
            list: A list of column names.
        """
        self.c.execute(f"PRAGMA table_info({table})")
        columns_info = self.c.fetchall()
        columns = [info[1] for info in columns_info]  # The second item in each row is the column name
        return columns

    def insert(self, table, row, format='tuple'):
        """
        Inserts data into the specified table in the SQLite database.
        
        Args:
            table (str): The name of the table where data will be inserted.
            row (tuple or dict): A tuple representing a single row of data or a dictionary where keys are column names.
            format (str, optional): The format of the input data ('tuple' or 'dict'). Defaults to 'tuple'.
        
        Returns:
            int: The ID of the inserted or existing record.
        """
        if format == 'dict':
            columns = row.keys()
            values = tuple(row.values())
        else:
            # If the format is 'tuple', we assume the columns need to be specified
            # The caller needs to provide the correct columns in the right order
            columns = self._get_columns_for_table(table)  # You need to implement this method to fetch the table's column names
            values = row
    
        # Create placeholders for the SQL queries
        placeholders = ', '.join('?' for _ in columns)
        
        # Build the SELECT query to check if the row already exists
        check_query = f'''
            SELECT id FROM {table}
            WHERE {' AND '.join([f"{col} = ?" for col in columns])}
        '''
        self.c.execute(check_query, values)
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
            self.c.execute(insert_query, values)
            # Get the ID of the newly inserted record
            return self.c.lastrowid

    def access(self, table='papers', select='*', limit=None, format='tuple'):
        """
        Accesses the specified table in the SQLite database and yields rows one at a time.
    
        Args:
            table (str): The name of the table to query. Defaults to 'papers'.
            select (str): The columns to select from the table. Defaults to '*', which selects all columns.
            limit (int, optional): The maximum number of rows to return. If None, all rows are returned.
            format (str, optional): Format of output, whether tuple or dict.
    
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
            if format=='tuple':
                yield row
            if format=='dict':
                yield self._tuple_to_dict(row)

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

