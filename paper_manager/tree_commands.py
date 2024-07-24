import sqlite3

import commands as pm

def get_parents(paper_tuple):
    child_id = paper_tuple[0]


    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    query = "SELECT child_id FROM citations WHERE child_id = ?"
    cursor.execute(query, (child_id,))
    
    citations = cursor.fetchall()
    conn.close()
    
    parent_ids = [parent_id[0] for parent_id in parent_ids]
    return [pm.grab(where=[('id',),(child_id,)]) for child_id in child_ids]

def get_children(paper_tuple):
    parent_id = paper_tuple[0]
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    query = "SELECT child_id FROM citations WHERE parent_id = ?"
    cursor.execute(query, (parent_id,))
    
    citations = cursor.fetchall()
    conn.close()
    
    child_ids = [child_id[0] for child_id in child_ids]
    return [grab(where=[('id',),(child_id,)]) for child_id in child_ids]
