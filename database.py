from flask import g 
import os
import sqlite3
from decimal import Decimal
from shutil import copyfileobj


DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "app.db")

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

#helper functions to insert decimals into the database as integers.
def decimal_to_int(dec:Decimal) -> int:
    return int(dec * 100)
def int_to_decimal(integer: int) -> Decimal:
    integer_str = str(integer)
    decimal_str = integer_str[:-2] + '.' + integer_str[-2:]
    return Decimal(decimal_str)
#NOTE: Conditions should not contain a WHERE in the beginning. Example: price>20. Wrong example: WHERE price>20  
def select_query(table:str, fields='*', *conditions:list, order_by=None, limit=None, offset=None):
    query = f"SELECT {', '.join(fields)} FROM {table}"
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    if order_by:
        query += f" ORDER BY {order_by}"
    if limit is not None:
        query += f" LIMIT {limit}"
    if offset is not None:
        query += f" OFFSET {offset}"
    return query
