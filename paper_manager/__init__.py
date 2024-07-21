from .commands import insert, access, edit, show_tables
from .embed_data import translate, SciBERT, update_scibert
from .setup_database import setup_database

__doc__ = """

insert(table='papers', *data:tuple)

access(table='papers', select='*', limit=None)

edit(table, function, condition=None)

show_tables()

translate(inputt:(torch.Tensor or str)) -> (str or torch.Tensor)

SciBERT.embed(self, text: str) -> torch.Tensor

setup_database(table_name='papers')


id INTEGER PRIMARY KEY,
title TEXT,
summary TEXT,
author TEXT,
year INTEGER,
category TEXT,
embedding BLOB

"""

