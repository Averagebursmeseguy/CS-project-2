import sqlite3
import os

con = sqlite3.connect("app.db")
con.execute("PRAGMA foreign_keys = ON;")

cursor = con.cursor()

cursor.execute("""CREATE TABLE users(
user_id INTEGER PRIMARY KEY AUTOINCREMENT,
 name TEXT NOT NULL,
 email TEXT NOT NULL UNIQUE
);""")

cursor.execute("""CREATE TABLE habits(
habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
set_by_id INTEGER NOT NULL,
title TEXT NOT NULL,
timespan TEXT NOT NULL,
FOREIGN KEY (set_by_id) REFERENCES users(user_id) ON DELETE CASCADE
)""")

cursor.execute("""CREATE TABLE goals(
goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
set_by_id INTEGER NOT NULL,
title TEXT NOT NULL,
state TEXT NOT NULL,
FOREIGN KEY (set_by_id) REFERENCES users(user_id) ON DELETE CASCADE
);""")