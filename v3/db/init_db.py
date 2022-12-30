import sqlite3 as sql

cn = sql.connect('database.db')

with open('schema.sql') as f:
    cn.executescript(f.read())

