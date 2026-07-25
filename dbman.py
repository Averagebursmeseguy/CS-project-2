import sqlite3

con = sqlite3.connect("app.db")
con.execute("PRAGMA foreign_keys = ON;")
cursor = con.cursor()

#adding passwords because i want to hurt people
cursor.execute("""CREATE TABLE users(
user_id INTEGER PRIMARY KEY AUTOINCREMENT,
 name TEXT NOT NULL,
 password TEXT NOT NULL,
 email VARCHAR NOT NULL UNIQUE
);""")

cursor.execute("""CREATE TABLE habits(
habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
set_by_id INTEGER NOT NULL,
title VARCHAR NOT NULL,
timespan TEXT NOT NULL,
FOREIGN KEY (set_by_id) REFERENCES users(user_id) ON DELETE CASCADE
)""")

cursor.execute("""CREATE TABLE goals(
goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
set_by_id INTEGER NOT NULL,
title VARCHAR NOT NULL,
state VARCHAR NOT NULL CHECK(state IN('Pending', 'In Progress', 'Completed')),
FOREIGN KEY (set_by_id) REFERENCES users(user_id) ON DELETE CASCADE
);""")

cursor.execute("""CREATE TABLE daily_logs(
log_id INTEGER PRIMARY KEY AUTOINCREMENT,
set_by_id INTEGER NOT NULL,
title VARCHAR NOT NULL,
content TEXT NOT NULL,
mood_score INTEGER CHECK(mood_score BETWEEN 1 AND 10),
FOREIGN KEY (set_by_id) REFERENCES users(user_id) ON DELETE CASCADE
);""")