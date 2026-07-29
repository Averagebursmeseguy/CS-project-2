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

#Seed data creation script

def make_dest_data():

    cursor.execute("""
    SELECT * FROM users where name = 'test_user'
    """)
    if cursor.fetchone():
        print('test data exists. Skipped making.')
        pass

    else:
        print('No test data. Making...')

        cursor.execute("""
        INSERT INTO users(name, password, email)
        VALUES('test_user', 'test_password_1234', 'bob@bobmail.com');
        """)

        cursor.execute("""
        INSERT INTO habits(set_by_id, title, quantitative, unit, timespan)
        VALUES(1, 'test habit 1', 'true', 'unit', 'daily');
        """)

        cursor.execute("""
        INSERT INTO habits(set_by_id, title, quantitative, unit, timespan)
        VALUES(1, 'test habit 2', 'false', NULL, 'weekly');
        """)

        cursor.execute("""
        INSERT INTO goals(set_by_id, title, state)
        VALUES(1, 'test goal 1', 'In Progress');
        """)

        cursor.execute("""
        INSERT INTO habit_logs(habit_id, timestamp, progress_quantity)
        VALUES(1, 1234567890, 2.2);
        """)

        cursor.execute("""
        INSERT INTO habit_logs(habit_id, timestamp, progress_quantity)
        VALUES(2, 1234567890, NULL);
        """)

        cursor.execute("""
        INSERT INTO daily_logs(set_by_id, title, content, mood_score)
        VALUES(1, 'log1', 'this is a test log used for testing', 5);
        """)

        cursor.execute("""
        INSERT INTO habit_logs(habit_id, timestamp, progress_quantity)
        VALUES(1, 1234567891, 3.5);
        """)

        cursor.execute("""
        INSERT INTO habit_logs(habit_id, timestamp, progress_quantity)
        VALUES(2, 1234567891, NULL);
        """)

        cursor.execute("""
        INSERT INTO habit_logs(habit_id, timestamp, progress_quantity)
        VALUES(1, 1234567892, 4.0);
        """)

        cursor.execute("""
        INSERT INTO habit_logs(habit_id, timestamp, progress_quantity)
        VALUES(2, 1234567892, NULL);
        """)

        cursor.execute("""
        INSERT INTO habit_logs(habit_id, timestamp, progress_quantity)
        VALUES(1, 1234567893, 1.8);
        """)


        cursor.execute("""
        INSERT INTO daily_logs(set_by_id, title, content, mood_score)
        VALUES(1, 'log2', 'Completed my habits and felt productive today.', 8);
        """)

        cursor.execute("""
        INSERT INTO daily_logs(set_by_id, title, content, mood_score)
        VALUES(1, 'log3', 'Had a busy day but managed to stay consistent.', 7);
        """)

        cursor.execute("""
        INSERT INTO daily_logs(set_by_id, title, content, mood_score)
        VALUES(1, 'log4', 'Missed one habit but reflected on what went wrong.', 5);
        """)

        cursor.execute("""
        INSERT INTO daily_logs(set_by_id, title, content, mood_score)
        VALUES(1, 'log5', 'Finished my goals early and had extra free time.', 9);
        """)

        cursor.execute("""
        INSERT INTO daily_logs(set_by_id, title, content, mood_score)
        VALUES(1, 'log6', 'Tried a new routine and tracked my progress.', 6);
        """)

        print('test data made')
        con.commit()

# Yes, I know this is injection attack galore. I do not care.
def fetch_unique(item, table, nocolumn) -> list[str] | list[tuple] | None:
    cursor.execute(f"""
    SELECT DISTINCT {item} FROM {table}
    """)

    if not nocolumn:
        return cursor.fetchall()
    if nocolumn:
        return [row[0] for row in cursor.fetchall()]

def fetch_table_info(table):
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [row[1] for row in cursor.fetchall()]
    return columns

def fetch_specific_data(table, column, query):
    cursor.execute(f"""
    SELECT {column} FROM {table} where {column} = {query}
    """)
    return cursor.fetchone

make_dest_data()

