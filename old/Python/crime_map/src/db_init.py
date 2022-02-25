#!/usr/bin/env python3
import sqlite3 as sql

connection = sql.connect("crimemap.sqlite3")
try:
    # sql = "CREATE DATABASE IF NOT EXISTS crimemap"
    # connection.execute(sql)
    sql = """CREATE TABLE IF NOT EXISTS crimes (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    latitude FLOAT(10,6),
    longitude FLOAT(10,6),
    date DATETIME,
    category VARCHAR(50),
    description VARCHAR(1000),
    updated_at TIMESTAMP
    );"""   
    connection.execute(sql)
    connection.commit()
finally:
    connection.close()
