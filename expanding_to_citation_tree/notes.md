
# Schema
So basically, I can keep the paper table as is, but add an additional parent/child table for the edges.
Each citation has a parent (cited), and a child (cited by). Both child and parents are many-to-many relationships.

```sql
CREATE TABLE citations (
    parent_id INT,
    child_id INT,
    PRIMARY KEY (parent_id, child_id),
    FOREIGN KEY (parent_id) REFERENCES papers(node_id),
    FOREIGN KEY (child_id) REFERENCES papers(node_id)
);
```

This can then be used to build both forward and backward trees.

# Python Functions

More elaborate functions will be needed in order to use the new table for the trees.

```python
from commands import grab

def get_parents(paper_tuple):
    child_id = paper_tuple[0]
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    query = "SELECT child_id FROM citations WHERE child_id = ?"
    cursor.execute(query, (child_id,))
    
    citations = cursor.fetchall()
    conn.close()
    
    parent_ids = [parent_id[0] for parent_id in parent_ids]
    return [grab(where=[('id',),(child_id,)]) for child_id in child_ids]

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
```
