import tkinter
from tkinter import ttk
import forms, dbman, visualizer

class Interface():
    def __init__(self, user) -> None:       
        self.logged_in_user_id = user
        self.frame_width = 1000
        self.frame_height = 600

        self.window = tkinter.Tk()
        self.window.geometry(f"{self.frame_width}x{self.frame_height}")
        self.window.title("CS habit tracker")

        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill = 'both', expand=True)
                        
        # Individual tab descriptions. Put your UI elements here
        self.frame1 = ttk.Frame(self.notebook, width=self.frame_width, height=self.frame_height)
        self.current_goal_indicator = ttk.Label(text="no goals running", font=forms.font, master=self.frame1)
        self.current_goal_indicator.pack()
        self.non_qualitatives_table = ttk.Treeview(master = self.frame1, columns=("Habit done", "Times done"), show="headings")
        self.non_qualitatives_table.pack()

        self.notebook.add(self.frame1, text="Dashboard")

        # Visualizer instance embedded in Dashboard (frame1)
        self.mood_graph = visualizer.WellnessVisualizer(self.frame1)


        self.frame2 = ttk.Frame(self.notebook, width=self.frame_width, height=self.frame_height)
        self.notebook.add(self.frame2, text="Log Progress")
        self.log_form = forms.DailyLog(self.frame2, self.logged_in_user_id)


        self.frame3 = ttk.Frame(self.notebook, width=self.frame_width, height=self.frame_height)
        self.notebook.add(self.frame3, text="Create Habit")
        self.habit_form = forms.HabitForm(self.frame3, current_user=self.logged_in_user_id)


        self.frame4 = ttk.Frame(self.notebook, width=self.frame_width, height=self.frame_height)
        self.notebook.add(self.frame4, text="History")

        self.notebook.bind("<<NotebookTabChanged>>", self.handle_tab_change)
        dbman.make_dest_data()

    def refresh_tab_1(self):
        # Updates the dashboard graphics and total goals count
        moods = dbman.fetch_column_by_user("daily_logs", "mood_score", self.logged_in_user_id)
        days = dbman.fetch_column_by_user('daily_logs', 'date_created', self.logged_in_user_id)

        if self.non_qualitatives_table.get_children() != ():
            for item in self.non_qualitatives_table.get_children():
                self.non_qualitatives_table.delete(item)

        for habit in dbman.get_count_non_qualitative_habits_user(self.logged_in_user_id):
            self.non_qualitatives_table.insert("", "end", values=habit)
        
        goals_being_done = dbman.count_columns_by_user('goal_id','goals', self.logged_in_user_id)
        self.current_goal_indicator.config(text=f'''{goals_being_done} goals total, {dbman.get_finished_tasks_user(self.logged_in_user_id)} done, {dbman.get_pending_tasks_user(self.logged_in_user_id)} pending, {dbman.get_in_progress_tasks_user(self.logged_in_user_id)} tasks in progress.''')
        
        self.mood_graph.draw_mood_trend(days, moods, 'mood graph')
        self.mood_graph.draw_habit_progress(dbman.get_total_habit_prgresses_with_unit_by_user(self.logged_in_user_id))


    def refresh_tab_2(self):
        # Dynamically changes habit log dropdown options.
        hobbies = dbman.fetch_unique('title', self.logged_in_user_id, 'habits', True)
        self.log_form.habit_to_log_entry.config(values=hobbies) #no idea what's wrong with this one. Pylance prolly trippin


    # Executes on tab change, used to call various helper scripts
    def handle_tab_change(self, event):
        selected_tab = self.notebook.tab(self.notebook.select(), 'text')
        match selected_tab:
            case "Log Progress":
                self.refresh_tab_2()

            case "Dashboard":
                self.refresh_tab_1()

    def run_interface(self):
        self.window.mainloop()

class LoginPanel():
    def __init__(self) -> None:
        self.login_window = tkinter.Tk()
        self.login_window.geometry(f"800x600")
        self.login_window.title("Login or Sign up")
        self.font = ('Times New Roman', 15)

        self.login_label = ttk.Label(font=self.font, text='Login or Sign up')
        self.login_label.pack()

        self.login_username_label = ttk.Label(font=self.font, text='Username')
        self.login_username_label.pack()

        self.login_username_entry = ttk.Entry(font=self.font)
        self.login_username_entry.pack()

        self.login_email_label = ttk.Label(font=self.font, text='Email')
        self.login_email_label.pack()
        
        self.login_email_entry = ttk.Entry(font=self.font)
        self.login_email_entry.pack()

        self.login_password_label = ttk.Label(font=self.font, text='Password')
        self.login_password_label.pack()
        
        self.login_password_entry = ttk.Entry(font=self.font)
        self.login_password_entry.pack()

        self.sign_in_button = ttk.Button(text="Log In", command=self.check_login)
        self.sign_in_button.pack(pady=10)

        self.sign_up_button = ttk.Button(text="Sign Up", command = self.check_sign_up)
        self.sign_up_button.pack(pady = 10)

    def run_login_window(self):
        self.login_window.mainloop()

    def check_login(self):
        password = self.login_password_entry.get()
        email = self.login_email_entry.get()
        username = self.login_username_entry.get()

        userID = dbman.check_user(username, password, email)

        if userID:
            self.login_window.destroy()
            app = Interface(userID)
            app.run_interface()

        else:
            print('error or sumn idk')

    def check_sign_up(self):
        password = self.login_password_entry.get()
        email = self.login_email_entry.get()
        username = self.login_username_entry.get()
        dbman.create_user(username, password, email)

