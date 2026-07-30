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
date_created TEXT NOT NULL,
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
        INSERT INTO daily_logs(set_by_id, title, content, date_created, mood_score)
        VALUES(1, 'log1', 'this is a test log used for testing', '2000-01-1', 5);
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
        INSERT INTO daily_logs(set_by_id, title, content, date_created, mood_score )
        VALUES(1, 'log2', 'Completed my habits and felt productive today.', '2000-01-02', 8);
        """)

        cursor.execute("""
        INSERT INTO daily_logs(set_by_id, title, content, date_created, mood_score)
        VALUES(1, 'log3', 'Had a busy day but managed to stay consistent.', '2000-01-03', 7);
        """)

        cursor.execute("""
        INSERT INTO daily_logs(set_by_id, title, content, date_created, mood_score)
        VALUES(1, 'log4', 'Missed one habit but reflected on what went wrong.', '2000-01-04', 5);
        """)

        cursor.execute("""
        INSERT INTO daily_logs(set_by_id, title, content, date_created, mood_score)
        VALUES(1, 'log5', 'Finished my goals early and had extra free time.', '2000-01-05', 6);
        """)

        cursor.execute("""
        INSERT INTO daily_logs(set_by_id, title, content, date_created, mood_score)
        VALUES(1, 'log6', 'Tried a new routine and tracked my progress.', '2000-01-06', 7);
        """)

        cursor.execute("""
        INSERT INTO goals(set_by_id, title, state)
        VALUES(1, 'Complete 30 day exercise streak', 'Pending');
        """)

        cursor.execute("""
        INSERT INTO goals(set_by_id, title, state)
        VALUES(1, 'Read 5 books this year', 'In Progress');
        """)

        cursor.execute("""
        INSERT INTO goals(set_by_id, title, state)
        VALUES(1, 'Maintain daily journaling habit', 'Completed');
        """)

        cursor.execute("""
        INSERT INTO goals(set_by_id, title, state)
        VALUES(1, 'Run a 10km race', 'Pending');
        """)

        cursor.execute("""
        INSERT INTO goals(set_by_id, title, state)
        VALUES(1, 'Improve sleep schedule', 'In Progress');
        """)

        cursor.execute("""
        INSERT INTO goals(set_by_id, title, state)
        VALUES(1, 'Drink enough water every day', 'Completed');
        """)

        cursor.execute("""
        INSERT INTO goals(set_by_id, title, state)
        VALUES(1, 'Learn Python advanced concepts', 'In Progress');
        """)

        cursor.execute("""
        INSERT INTO goals(set_by_id, title, state)
        VALUES(1, 'Meditate consistently for a month', 'Pending');
        """)

        cursor.execute("""
        INSERT INTO habits(set_by_id, title, quantitative, unit, timespan)
        VALUES(1, 'Drink Water', 'true', 'litres', 'daily');
        """)

        cursor.execute("""
        INSERT INTO habits(set_by_id, title, quantitative, unit, timespan)
        VALUES(1, 'Meditate', 'true', 'minutes', 'daily');
        """)

        cursor.execute("""
        INSERT INTO habit_logs(habit_id, timestamp, progress_quantity)
        VALUES(3, 1234567890, 1.8);
        """)

        cursor.execute("""
        INSERT INTO habit_logs(habit_id, timestamp, progress_quantity)
        VALUES(4, 1234567890, 10);
        """)

        cursor.execute("""
        INSERT INTO habit_logs(habit_id, timestamp, progress_quantity)
        VALUES(3, 1234567891, 2.1);
        """)

        cursor.execute("""
        INSERT INTO habit_logs(habit_id, timestamp, progress_quantity)
        VALUES(4, 1234567891, 15);
        """)

        cursor.execute("""
        INSERT INTO habit_logs(habit_id, timestamp, progress_quantity)
        VALUES(3, 1234567892, 2.5);
        """)

        cursor.execute("""
        INSERT INTO habit_logs(habit_id, timestamp, progress_quantity)
        VALUES(4, 1234567892, 20);
        """)

        cursor.execute("""
        INSERT INTO habit_logs(habit_id, timestamp, progress_quantity)
        VALUES(3, 1234567893, 1.9);
        """)

        cursor.execute("""
        INSERT INTO habit_logs(habit_id, timestamp, progress_quantity)
        VALUES(4, 1234567893, 12);
        """)

        cursor.execute("""
        INSERT INTO habit_logs(habit_id, timestamp, progress_quantity)
        VALUES(3, 1234567894, 2.3);
        """)

        cursor.execute("""
        INSERT INTO habit_logs(habit_id, timestamp, progress_quantity)
        VALUES(4, 1234567894, 18);
        """)

        cursor.execute("""
        INSERT INTO habit_logs(habit_id, timestamp, progress_quantity)
        VALUES(3, 1234567895, 2.0);
        """)

        cursor.execute("""
        INSERT INTO habit_logs(habit_id, timestamp, progress_quantity)
        VALUES(4, 1234567895, 25);
        """)

        print('test data made')
        con.commit()


def fetch_unique(item, user, table, nocolumn) -> list[str] | list[tuple] | None:
    cursor.execute(f"""
    SELECT DISTINCT {item} FROM {table} WHERE set_by_id = ?
    """, (user,))

    if not nocolumn:
        return cursor.fetchall()
    if nocolumn:
        return [row[0] for row in cursor.fetchall()]

def count_columns_by_user(column_to_count, table, userID):
    cursor.execute(f"""
    SELECT COUNT ({column_to_count}) FROM {table} WHERE set_by_id = ?
    """, (userID,))
    return cursor.fetchone()[0]

def fetch_column_by_user(table, column, userID):
    cursor.execute(f"""
    SELECT {column} from {table} WHERE set_by_id = ?
    """, (userID,))
    return [row[0] for row in cursor.fetchall()]

def fetch_table_info(table):
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [row[1] for row in cursor.fetchall()]
    return columns

def fetch_specific_data(table, column, query):
    cursor.execute(f"""
    SELECT {column} FROM {table} where {column} = ?
    """, (query,))
    return cursor.fetchone()[0]

#That's it I give up trying to larp having an ORM. Lost too many braincells. Specifics galore.
def create_new_habit(user, title, quantitative, unit, timespan):
    print(f'{user}, {title}, {quantitative}, {unit}, {timespan}')
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
    if result != None:
        target_id = result[0]
    else:
        return

    cursor.execute("""
    INSERT INTO habit_logs(habit_id, timestamp, progress_quantity)
    VALUES (?, ?, ?)
    """, (target_id, timestamp, progress_quantity))

    con.commit()

def get_finished_tasks_user(user):
    cursor.execute("""
    SELECT COUNT (*) FROM goals WHERE set_by_id = ? AND state = 'Completed'
    """, (user,))
    return cursor.fetchone()[0]

def get_pending_tasks_user(user):
    cursor.execute("""
        SELECT COUNT(*)
        FROM goals
        WHERE set_by_id = ?
          AND state = 'Pending'
    """, (user,))
    return cursor.fetchone()[0]

def get_in_progress_tasks_user(user):
    cursor.execute("""
        SELECT COUNT(*)
        FROM goals
        WHERE set_by_id = ?
          AND state = 'In Progress'
    """, (user,))
    return cursor.fetchone()[0]

def get_total_habit_prgresses_with_unit_by_user(user):
    cursor.execute('''
    SELECT habits.title, SUM(habit_logs.progress_quantity), habits.unit
    FROM habit_logs
    JOIN habits
    ON habit_logs.habit_id = habits.habit_id
    WHERE habits.quantitative = 'true' AND set_by_id = ?
    GROUP BY habits.title
    ''', (user,))
    return cursor.fetchall()

def get_count_non_qualitative_habits_user(user):
    cursor.execute("""
    SELECT habits.title, COUNT(habit_logs.habit_log_id) AS log_count FROM habits
    LEFT JOIN habit_logs
    ON habits.habit_id = habit_logs.habit_id
    WHERE habits.set_by_id = ? AND habits.quantitative = 'false'
    GROUP BY habits.habit_id, habits.title;
    """,(user, ))
    return cursor.fetchall()

def create_user(username, password, email):
    cursor.execute("""
    INSERT INTO users(name, password, email)
    VALUES (?, ?, ?)
    """, (username, password, email))

    con.commit()

def check_user(username, password, email):
    cursor.execute("""
    SELECT user_id FROM users
    WHERE name = ? AND password = ? AND email = ?
    """, (username, password, email))

    result = cursor.fetchone()

    if result:
        return result[0]  # return user_id
    else:
        return None

def get_goals_by_user(user):
    cursor.execute("""
    SELECT title, state
    FROM goals
    WHERE set_by_id = ?
    """, (user,))

    return cursor.fetchall()

def get_goals_with_id_by_user(user):
    cursor.execute("""
    SELECT goal_id, title, state
    FROM goals
    WHERE set_by_id = ?
    """, (user,))

    return cursor.fetchall()

def get_goal_by_id(goal_id):
    cursor.execute("""
    SELECT goal_id, title, state
    FROM goals
    WHERE goal_id = ?
    """, (goal_id,))

    return cursor.fetchone()

def get_log_by_user(user):
    cursor.execute("""
    SELECT title, date_created
    FROM daily_logs
    WHERE set_by_id = ?
    """, (user,))

    return cursor.fetchall()

def get_log_with_id_by_user(user):
    cursor.execute("""
    SELECT log_id, title, date_created
    FROM daily_logs
    WHERE set_by_id = ?
    """, (user,))

    return cursor.fetchall()

def get_log_details_by_id(log_id):
    cursor.execute("""
    SELECT log_id, title, content, date_created, mood_score
    FROM daily_logs
    WHERE log_id = ?
    """, (log_id,))

    return cursor.fetchone()

def create_new_goal(set_by, title, state):
    cursor.execute("""
    INSERT INTO goals(set_by_id, title, state)

    VALUES (?, ?, ?)
    """, (set_by, title, state))

def update_goal(goal_id, title, state):
    cursor.execute("""
    UPDATE goals
    SET title = ?, state = ?
    WHERE goal_id = ?
    """, (title, state, goal_id))

    con.commit()

def delete_goal(goal_id):
    cursor.execute("""
    DELETE FROM goals
    WHERE goal_id = ?
    """, (goal_id,))

    con.commit()

def update_daily_log(log_id, title, content, mood):
    cursor.execute("""
    UPDATE daily_logs
    SET title = ?,
        content = ?,
        mood_score = ?
    WHERE log_id = ?
    """, (title, content, mood, log_id))

    con.commit()

def delete_daily_log(log_id):
    cursor.execute("""
    DELETE FROM daily_logs
    WHERE log_id = ?
    """, (log_id,))

    con.commit()