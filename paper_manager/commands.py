

import sqlite3
import traceback

class db:
    def __init__(self, db_file='science_papers.db'):
        self.db_file = db_file
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()
        self._create_tables()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is None:
            self.connection.commit()
        else:
            traceback.print_exception(exc_type, exc_value, tb)
        if self.connection:
            self.connection.close()

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
            self.cursor.execute(query)

    def _get_column_names(self, table_name):
        match table_name:
            case 'authors':
                return  ['id', 'name']
            case 'author_papers':
                return ['id', 'title', 'summary', 'year', 'author_id', 'embedding']
            case 'paper_references':
                return ['parent_id', 'child_id', 'weighting']
            case 'citation_papers':
                return ['id', 'title', 'summary', 'author', 'year', 'category', 'embedding', 'cited_by', 'cites', 'c_vector', 'c_mag']
        return ['id', 'title', 'summary', 'author', 'year', 'category', 'embedding'] # default


    def _tuple_to_dict(self, row, table_name='papers'):
        return dict(zip(self._get_column_names(table_name), row))

    def _dict_to_tuple(self, dictionary, table_name='papers'):
        return tuple(dictionary.get(column, None) for column in self._get_column_names(table_name))

    def insert(self, record, table_name='papers', input_format='tuple'):
        try:
            # Automatically rename 'authors' to 'author' if present in the record
            if input_format == 'dict':
                if 'authors' in record:
                    record['author'] = record.pop('authors')
                
                # Get the actual columns from the database
                self.cursor.execute(f'PRAGMA table_info({table_name})')
                table_columns = [info[1] for info in self.cursor.fetchall()]
                
                # Filter out any keys that aren't actual columns
                filtered_record = {key: record.get(key, None) for key in table_columns}
                
                columns = filtered_record.keys()
                values = tuple(filtered_record.values())
            else:
                columns = self._get_column_names(table_name)
                values = record
    
            placeholders = ', '.join('?' for _ in columns)
    
            # Adjust the check query to only use the provided keys
            check_query = f'SELECT id FROM {table_name} WHERE {" AND ".join([f"{col} = ?" for col in columns])}'
            
            try:
                self.cursor.execute(check_query, values)
                existing_record = self.cursor.fetchone()
            except sqlite3.OperationalError as e:
                print(f"Error executing query: {e}")
                return None
    
            if existing_record:
                return existing_record[0]
            else:
                try:
                    insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                    self.cursor.execute(insert_query, values)
                    return self.cursor.lastrowid
                except sqlite3.OperationalError as e:
                    print(f"Error executing insert: {e}")
                    return None
        except Exception as e:
            # Catch any exception, print the error, and continue
            print(f"An error occurred: {e}")
            return None

    def fetch(self, table_name='papers', select='*', where_conditions=None, limit=None, output_format='tuple'):
        """Accesses the specified table in the SQLite database and yields rows one at a time."""
        query = f'SELECT {select} FROM {table_name}'
        if where_conditions:
            query += ' WHERE ' + ' AND '.join([f"{column} = ?" for column in where_conditions[0]])

        if limit:
            query += f' LIMIT {limit}'
        
        self.cursor.execute(query, where_conditions[1] if where_conditions else ())
    
        while (row := self.cursor.fetchone()) is not None:
            yield self._tuple_to_dict(row, table_name) if output_format == 'dict' else row

    def fetch_one(self, table_name='papers', select='*', where_conditions=None, output_format='tuple'):
        """ Fetches a single row based on the specified conditions. """
        query = f'SELECT {select} FROM {table_name}'
        if where_conditions:
            query += ' WHERE ' + ' AND '.join([f"{column} = ?" for column in where_conditions[0]])
        
        query += ' LIMIT 1'
    
        self.cursor.execute(query, where_conditions[1] if where_conditions else ())
        row = self.cursor.fetchone()
        return self._tuple_to_dict(row, table_name) if output_format == 'dict' else row

    def update(self, table_name, update_function, condition=None):
        """ Updates every row that meets a condition by the update_function """
        query = f'SELECT * FROM {table_name}'
        if condition:
            query += f' WHERE {condition}'
        
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
    
        column_names = [description[0] for description in self.cursor.description]
    
        for row in rows:
            new_row = update_function(row)
    
            set_clause = ', '.join(f"{col} = ?" for col in column_names[1:])
    
            self.cursor.execute(f' UPDATE {table_name} SET {set_clause} WHERE {column_names[0]} = ?  ', new_row[1:] + (row[0],))

    def list_tables(self):
        """
        Returns a list of all table names in the SQLite database.
    
        Returns:
            list: A list of table names.
        """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [table[0] for table in self.cursor.fetchall()]

