from .commands import db
#import tree_commands as tree
from .embed_data import translate, SciBERT, update_scibert
#from .setup_database import setup_database

__doc__ = """


with pm.db() as db:
    db.insert(table='papers', *data:tuple)
    
    db.access(table='papers', select='*', limit=None)
    
    db.edit(table, function, condition=None)
    
    db.show_tables()

pm.translate(inputt:(torch.Tensor or str)) -> (str or torch.Tensor)

bert = pm.SciBERT()

bert.embed(self, text: str) -> torch.Tensor

pm.update_scibert(table='papers') # updates all raw embeddings in table.

pm.setup_database(table_name='papers')

pm.tree.get_parents(paper_tuple)

pm.tree.get_children(paper_tuple)

id INTEGER PRIMARY KEY,
title TEXT,
summary TEXT,
author TEXT,
year INTEGER,
category TEXT,
embedding BLOB

"""

