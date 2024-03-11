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
#NOTE: Conditions should not contain a WHERE in the beginning
def select_query(table:str, fields='*', *conditions:list, order_by=None, limit=None, offset=None,like_conditions=None):
    params = []
    query = f"SELECT {', '.join(fields)} FROM {table}"
    #could be optimized by joining the lists and value and keeping the order.
    if conditions:
        fields, vals = split_conditions(conditions)
        query += " WHERE " + " AND ".join(fields)
        params.extend(vals)
        if like_conditions:
            q,v = split_like_conditions(like_conditions)
            query += " AND "+" OR ".join(q)
            params.extend(v)
    elif like_conditions:
        q,v = split_like_conditions(like_conditions)
        query += " WHERE "+" OR ".join(q)
        params.extend(v)
    if order_by:
        query += f" ORDER BY ?"
        params.append(order_by)
    if limit is not None:
        query += f" LIMIT ?"
        params.append(limit)
    if offset is not None:
        query += f" OFFSET ?"
        params.append(offset)
    return query,params

def select_in_query(items:list, table:str, fields:list) -> str:
    items_str = ', '.join('?' * len(items))
    fields_str = ', '.join(fields)
    return f"SELECT {fields_str} FROM {table} WHERE id IN ({items_str})", items

#creates two arrays from [field=val] : [field=?] and [val] where field and val are variables
#Eww
def split_conditions(conditions):
    fields = []
    values = []
    for condition in conditions:
        print(conditions)
        s = condition.split('=')
        fields.append(s[0]+"=?")
      
        values.append(s[1].strip())
    return fields, values

def split_like_conditions(like_conditions):
    query = []
    values = []
    for condition in like_conditions:
        split = condition.split("'")
        text = split[1]
        start = split[0] + " ? "
        query.append(start)
        values.append(text)
    return query, values