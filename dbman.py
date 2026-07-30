import sqlite3

con = sqlite3.connect("app.db")
con.execute("PRAGMA foreign_keys = ON;")
cursor = con.cursor()

# Schema Initialization
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
);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS habit_logs(
    habit_log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id INTEGER NOT NULL,
    timestamp INTEGER NOT NULL,
    progress_quantity REAL CHECK((progress_quantity IS NULL OR progress_quantity >= 0.0)),
    FOREIGN KEY (habit_id) REFERENCES habits (habit_id) ON DELETE CASCADE
);""")

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
    date_created TEXT NOT NULL,
    mood_score INTEGER CHECK(mood_score BETWEEN 1 AND 10),
    FOREIGN KEY (set_by_id) REFERENCES users(user_id) ON DELETE CASCADE
);""")
con.commit()

# Seed Data Initialization
def make_dest_data():
    cursor.execute("SELECT * FROM users WHERE name = 'test_user'")
    if cursor.fetchone():
        print('Test data exists. Skipped making.')
        return

    print('No test data found. Seeding records...')
    cursor.execute("INSERT INTO users(name, password, email) VALUES('test_user', 'test_password_1234', 'bob@bobmail.com');")
    cursor.execute("INSERT INTO habits(set_by_id, title, quantitative, unit, timespan) VALUES(1, 'test habit 1', 'true', 'unit', 'daily');")
    cursor.execute("INSERT INTO habits(set_by_id, title, quantitative, unit, timespan) VALUES(1, 'test habit 2', 'false', NULL, 'weekly');")
    cursor.execute("INSERT INTO goals(set_by_id, title, state) VALUES(1, 'test goal 1', 'In Progress');")
    
    cursor.execute("INSERT INTO habit_logs(habit_id, timestamp, progress_quantity) VALUES(1, 1234567890, 2.2);")
    cursor.execute("INSERT INTO habit_logs(habit_id, timestamp, progress_quantity) VALUES(2, 1234567890, NULL);")
    
    cursor.execute("INSERT INTO daily_logs(set_by_id, title, content, date_created, mood_score) VALUES(1, 'log1', 'this is a test log used for testing', '2000-01-01', 5);")
    cursor.execute("INSERT INTO daily_logs(set_by_id, title, content, date_created, mood_score) VALUES(1, 'log2', 'Completed my habits and felt productive today.', '2000-01-02', 8);")
    cursor.execute("INSERT INTO daily_logs(set_by_id, title, content, date_created, mood_score) VALUES(1, 'log3', 'Had a busy day but managed to stay consistent.', '2000-01-03', 7);")

    con.commit()
    print('Test data generated successfully.')

# Query Utilities
def fetch_unique(item, user, table, nocolumn):
    # Allowed white-listed entities to avoid raw format injection
    allowed_tables = {"users", "habits", "habit_logs", "goals", "daily_logs"}
    allowed_items = {"title", "name", "email", "unit", "timespan"}
    if table not in allowed_tables or item not in allowed_items:
        raise ValueError("Invalid table or column query requested.")

    cursor.execute(f"SELECT DISTINCT {item} FROM {table} WHERE set_by_id = ?", (user,))
    rows = cursor.fetchall()
    return [row[0] for row in rows] if nocolumn else rows

def count_columns_by_user(column_to_count, table, userID):
    allowed_tables = {"users", "habits", "habit_logs", "goals", "daily_logs"}
    allowed_cols = {"goal_id", "habit_id", "log_id", "user_id"}
    if table not in allowed_tables or column_to_count not in allowed_cols:
        raise ValueError("Invalid entity parameters.")

    cursor.execute(f"SELECT COUNT({column_to_count}) FROM {table} WHERE set_by_id = ?", (userID,))
    res = cursor.fetchone()
    return res[0] if res else 0

def fetch_column_by_user(table, column, userID):
    allowed_tables = {"users", "habits", "habit_logs", "goals", "daily_logs"}
    allowed_cols = {"title", "date_created", "mood_score", "state"}
    if table not in allowed_tables or column not in allowed_cols:
        raise ValueError("Invalid query target.")

    cursor.execute(f"SELECT {column} FROM {table} WHERE set_by_id = ?", (userID,))
    return [row[0] for row in cursor.fetchall()]

# Data Mutation Functions
def create_new_habit(user, title, quantitative, unit, timespan):
    cursor.execute("""
    INSERT INTO habits(set_by_id, title, quantitative, unit, timespan)
    VALUES (?, ?, ?, ?, ?);
    """, (user, title, quantitative, unit, timespan))
    con.commit()

def create_new_daily_log(user, title, content, mood):
    cursor.execute("""
    INSERT INTO daily_logs(set_by_id, title, content, date_created, mood_score)
    VALUES (?, ?, ?, DATE('now'), ?)
    """, (user, title, content, mood))
    con.commit()

def create_new_habit_progress(user, title, timestamp, progress_quantity):
    cursor.execute("SELECT habit_id FROM habits WHERE title = ? AND set_by_id = ?", (title, user))
    result = cursor.fetchone()
    if result:
        target_id = result[0]
        cursor.execute("""
        INSERT INTO habit_logs(habit_id, timestamp, progress_quantity)
        VALUES (?, ?, ?)
        """, (target_id, timestamp, progress_quantity))
        con.commit()

def get_finished_tasks_user(user):
    cursor.execute("SELECT COUNT(*) FROM goals WHERE set_by_id = ? AND state = 'Completed'", (user,))
    return cursor.fetchone()[0]

def get_pending_tasks_user(user):
    cursor.execute("SELECT COUNT(*) FROM goals WHERE set_by_id = ? AND state = 'Pending'", (user,))
    return cursor.fetchone()[0]

def get_in_progress_tasks_user(user):
    cursor.execute("SELECT COUNT(*) FROM goals WHERE set_by_id = ? AND state = 'In Progress'", (user,))
    return cursor.fetchone()[0]

def get_total_habit_prgresses_with_unit_by_user(user):
    cursor.execute('''
    SELECT habits.title, SUM(habit_logs.progress_quantity), habits.unit
    FROM habit_logs
    JOIN habits ON habit_logs.habit_id = habits.habit_id
    WHERE habits.quantitative = 'true' AND set_by_id = ?
    GROUP BY habits.title
    ''', (user,))
    return cursor.fetchall()

def get_count_non_qualitative_habits_user(user):
    cursor.execute("""
    SELECT habits.title, COUNT(habit_logs.habit_log_id) AS log_count FROM habits
    LEFT JOIN habit_logs ON habits.habit_id = habit_logs.habit_id
    WHERE habits.set_by_id = ? AND habits.quantitative = 'false'
    GROUP BY habits.habit_id, habits.title;
    """, (user,))
    return cursor.fetchall()

def get_goals_by_user(user):
    cursor.execute("SELECT title, state FROM goals WHERE set_by_id = ?", (user,))
    return cursor.fetchall()

def get_goals_with_id_by_user(user):
    cursor.execute("SELECT goal_id, title, state FROM goals WHERE set_by_id = ?", (user,))
    return cursor.fetchall()

def get_goal_by_id(goal_id):
    cursor.execute("SELECT goal_id, title, state FROM goals WHERE goal_id = ?", (goal_id,))
    return cursor.fetchone()

def get_log_with_id_by_user(user):
    cursor.execute("SELECT log_id, title, date_created FROM daily_logs WHERE set_by_id = ?", (user,))
    return cursor.fetchall()

def get_log_details_by_id(log_id):
    cursor.execute("SELECT log_id, title, content, date_created, mood_score FROM daily_logs WHERE log_id = ?", (log_id,))
    return cursor.fetchone()

def update_goal(goal_id, title, state):
    cursor.execute("UPDATE goals SET title = ?, state = ? WHERE goal_id = ?", (title, state, goal_id))
    con.commit()

def delete_goal(goal_id):
    cursor.execute("DELETE FROM goals WHERE goal_id = ?", (goal_id,))
    con.commit()

def update_daily_log(log_id, title, content, mood):
    cursor.execute("UPDATE daily_logs SET title = ?, content = ?, mood_score = ? WHERE log_id = ?", (title, content, mood, log_id))
    con.commit()

def delete_daily_log(log_id):
    cursor.execute("DELETE FROM daily_logs WHERE log_id = ?", (log_id,))
    con.commit()
