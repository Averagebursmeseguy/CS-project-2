import sqlite3

con = sqlite3.connect("app.db")
con.execute("PRAGMA foreign_keys = ON;")
cursor = con.cursor()

#adding passwords because *someone* has to learn about salting and encrypt
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
user_id INTEGER PRIMARY KEY AUTOINCREMENT,
 name TEXT NOT NULL,
 password TEXT NOT NULL,
 email VARCHAR NOT NULL UNIQUE
);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS habits(
habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
set_by_id INTEGER NOT NULL,
title VARCHAR NOT NULL,
quantitative VARCHAR NOT NULL CHECK(quantitative IN('true', 'false')),
unit VARCHAR,
timespan TEXT NOT NULL CHECK(timespan IN ('daily', 'weekly', 'monthly', 'yearly')),
CHECK((quantitative = 'true' AND unit IS NOT NULL) OR (quantitative = 'false' AND unit IS NULL)),

FOREIGN KEY (set_by_id) REFERENCES users(user_id) ON DELETE CASCADE
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS habit_logs(
habit_log_id INTEGER PRIMARY KEY AUTOINCREMENT,
habit_id INTEGER NOT NULL,
timestamp INTEGER NOT NULL,
progress_quantity REAL CHECK((progress_quantity IS NULL OR progress_quantity >= 0.0)),

FOREIGN KEY (habit_id) REFERENCES habits (habit_id) ON DELETE CASCADE
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS goals(
goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
set_by_id INTEGER NOT NULL,
title VARCHAR NOT NULL,
state VARCHAR NOT NULL CHECK(state IN('Pending', 'In Progress', 'Completed')),

FOREIGN KEY (set_by_id) REFERENCES users(user_id) ON DELETE CASCADE
);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS daily_logs(
log_id INTEGER PRIMARY KEY AUTOINCREMENT,
set_by_id INTEGER NOT NULL,
title VARCHAR NOT NULL,
content TEXT NOT NULL,
mood_score INTEGER CHECK(mood_score BETWEEN 1 AND 10),

FOREIGN KEY (set_by_id) REFERENCES users(user_id) ON DELETE CASCADE
);""")

def fetch_table_info(table):
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [row[1] for row in cursor.fetchall()]
    return columns