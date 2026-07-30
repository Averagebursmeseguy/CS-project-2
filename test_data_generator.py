
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