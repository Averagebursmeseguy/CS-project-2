import tkinter
from tkinter import ttk, messagebox
import forms, dbman, visualizer

class GoalEditDialog(tkinter.Toplevel):
    def __init__(self, parent, goal_id, current_title, current_state, on_success):
        super().__init__(parent)
        self.title("Update Goal")
        self.geometry("400x220")
        self.goal_id = goal_id
        self.on_success = on_success

        ttk.Label(self, text="Goal Title:", font=forms.font).pack(pady=5)
        self.title_entry = ttk.Entry(self, font=forms.font, width=30)
        self.title_entry.insert(0, current_title)
        self.title_entry.pack(pady=5)

        ttk.Label(self, text="Status:", font=forms.font).pack(pady=5)
        self.state_combobox = ttk.Combobox(self, state="readonly", values=['Pending', 'In Progress', 'Completed'])
        self.state_combobox.set(current_state)
        self.state_combobox.pack(pady=5)

        ttk.Button(self, text="Save Changes", command=self.save).pack(pady=15)

    def save(self):
        new_title = self.title_entry.get().strip()
        new_state = self.state_combobox.get()
        if not new_title:
            messagebox.showwarning("Warning", "Title cannot be empty.")
            return
        dbman.update_goal(self.goal_id, new_title, new_state)
        self.on_success()
        self.destroy()

class LogEditDialog(tkinter.Toplevel):
    def __init__(self, parent, log_id, current_title, current_content, current_mood, on_success):
        super().__init__(parent)
        self.title("Update Daily Log")
        self.geometry("500x420")
        self.log_id = log_id
        self.on_success = on_success

        ttk.Label(self, text="Log Title:", font=forms.font).pack(pady=5)
        self.title_entry = ttk.Entry(self, font=forms.font, width=35)
        self.title_entry.insert(0, current_title)
        self.title_entry.pack(pady=5)

        ttk.Label(self, text="Mood (1 - 10):", font=forms.font).pack(pady=5)
        self.mood_scale = ttk.Scale(self, from_=1, to=10)
        if current_mood is not None:
            self.mood_scale.set(current_mood)
        else:
            self.mood_scale.set(5)
        self.mood_scale.pack(pady=5)

        ttk.Label(self, text="Content:", font=forms.font).pack(pady=5)
        self.content_text = tkinter.Text(self, height=8, width=45, wrap="word")
        self.content_text.insert("1.0", current_content if current_content else "")
        self.content_text.pack(pady=5)

        ttk.Button(self, text="Save Changes", command=self.save).pack(pady=15)

    def save(self):
        new_title = self.title_entry.get().strip()
        new_content = self.content_text.get("1.0", "end-1c")
        new_mood = round(self.mood_scale.get())
        if not new_title:
            messagebox.showwarning("Warning", "Title cannot be empty.")
            return
        dbman.update_daily_log(self.log_id, new_title, new_content, new_mood)
        self.on_success()
        self.destroy()

class Interface():
    def __init__(self, user) -> None:       
        self.logged_in_user_id = user
        self.frame_width = 1500
        self.frame_height = 800

        self.window = tkinter.Tk()
        self.window.geometry(f"{self.frame_width}x{self.frame_height}")
        self.window.title("CS habit tracker")

        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill = 'both', expand=True)
                        
        # Individual tab descriptions. Put your UI elements here
        self.frame1 = ttk.Frame(self.notebook, width=self.frame_width, height=self.frame_height)
        self.current_goal_indicator = ttk.Label(text="no goals running", font=forms.font, master=self.frame1)
        self.current_goal_indicator.grid(row = 0, column = 0)

        self.non_qualitatives_table = ttk.Treeview(master = self.frame1, columns=("Habit done", "Times done"), show="headings")
        self.non_qualitatives_table.heading("Habit done", text='Habit done')
        self.non_qualitatives_table.heading('Times done', text="Times Done")
        self.non_qualitatives_table.grid(row = 1, column= 1)

        self.goal_table = ttk.Treeview(master = self.frame1, columns=('Goals', 'Status'), show='headings')
        self.goal_table.heading('Goals', text='Goal')
        self.goal_table.heading('Status', text='Status')
        self.goal_table.grid(row = 1, column=0)

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

        #historty label
        self.history_tab_label = ttk.Label(master=self.frame4,font=('Times New Roman', 20), text="History")
        self.history_tab_label.grid(row=0, column=1)

        #Goal table for history
        self.history_goal_table = ttk.Treeview(master = self.frame4, columns=('Goals', 'Status'), show='headings')
        self.history_goal_table.heading('Goals', text='Goal')
        self.history_goal_table.heading('Status', text='Status')
        self.history_goal_table.grid(row = 1, column=0)

        #log table
        self.history_log_table = ttk.Treeview(master = self.frame4, columns=('1', '2'), show='headings')
        self.history_log_table.heading('1', text="Title")
        self.history_log_table.heading('2', text='Date Created')
        self.history_log_table.grid(row=1, column=2)

        #goal selector
        self.goal_selector = ttk.Combobox(
        self.frame4,
        state="readonly",
        width=30
        )
        self.goal_selector.config(
        values=dbman.fetch_column_by_user(
        "goals",
        "title",
        self.logged_in_user_id
        )
        )
        self.goal_selector.grid(row=2, column=0)

        #log selector
        self.log_selector = ttk.Combobox(
        self.frame4,
        state="readonly",
        width=30
        )
        self.log_selector.config(
        values=dbman.fetch_column_by_user(
        "daily_logs",
        "title",
        self.logged_in_user_id
        )
        )
        self.log_selector.grid(row=2, column=2)

        #log viewer
        self.log_content_view = tkinter.Text(
            self.frame4,
            width=60,
            height=15,
            wrap="word"
        )
        self.log_content_view.grid(row = 3, column=2)

        self.goal_map = {}
        self.log_map = {}

        self.history_goal_table.bind("<<TreeviewSelect>>", self.on_goal_treeview_select)
        self.history_log_table.bind("<<TreeviewSelect>>", self.on_log_treeview_select)
        self.goal_selector.bind("<<ComboboxSelected>>", self.on_goal_combobox_select)
        self.log_selector.bind("<<ComboboxSelected>>", self.on_log_combobox_select)

        self.goal_update_button = ttk.Button(
            self.frame4,
            text="Update Goal",
            command=self.handle_update_goal
            )
        self.goal_update_button.grid(row=3, column=0)

        self.goal_delete_button = ttk.Button(
            self.frame4,
            text="Delete Goal",
            command=self.handle_delete_goal
            )
        self.goal_delete_button.grid(row=4, column=0)

        self.log_update_button = ttk.Button(
            self.frame4,
            text="Update Log",
            command=self.handle_update_log
            )
        self.log_update_button.grid(row=4, column=2)

        self.log_delete_button = ttk.Button(
            self.frame4,
            text="Delete Log",
            command=self.handle_delete_log
            )
        self.log_delete_button.grid(row=5, column=2)

        #bindings and things 
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

        for item in self.goal_table.get_children():
            self.goal_table.delete(item)

        for goal in dbman.get_goals_by_user(self.logged_in_user_id):
            self.goal_table.insert(
                "",
                "end",
                values=goal
            )
        
        goals_being_done = dbman.count_columns_by_user('goal_id','goals', self.logged_in_user_id)
        self.current_goal_indicator.config(text=f'''{goals_being_done} goals total, {dbman.get_finished_tasks_user(self.logged_in_user_id)} done, {dbman.get_pending_tasks_user(self.logged_in_user_id)} pending, {dbman.get_in_progress_tasks_user(self.logged_in_user_id)} tasks in progress.''')
        
        self.mood_graph.draw_mood_trend(days, moods, 'mood graph')
        self.mood_graph.draw_habit_progress(dbman.get_total_habit_prgresses_with_unit_by_user(self.logged_in_user_id))


    def refresh_tab_2(self):
        # Dynamically changes habit log dropdown options.
        hobbies = dbman.fetch_unique('title', self.logged_in_user_id, 'habits', True)
        self.log_form.habit_to_log_entry.config(values=hobbies) #no idea what's wrong with this one. Pylance prolly trippin

    def refresh_tab_4(self):
        for item in self.history_goal_table.get_children():
            self.history_goal_table.delete(item)

        self.goal_map = {}
        goals_data = dbman.get_goals_with_id_by_user(self.logged_in_user_id)
        goal_titles = []
        for goal_id, title, state in goals_data:
            self.history_goal_table.insert("", "end", iid=str(goal_id), values=(title, state))
            self.goal_map[title] = goal_id
            goal_titles.append(title)

        self.goal_selector.config(values=goal_titles)

        for item in self.history_log_table.get_children():
            self.history_log_table.delete(item)

        self.log_map = {}
        logs_data = dbman.get_log_with_id_by_user(self.logged_in_user_id)
        log_titles = []
        for log_id, title, date_created in logs_data:
            self.history_log_table.insert("", "end", iid=str(log_id), values=(title, date_created))
            self.log_map[title] = log_id
            log_titles.append(title)

        self.log_selector.config(values=log_titles)

    def get_selected_goal_id(self):
        selected_items = self.history_goal_table.selection()
        if selected_items:
            return int(selected_items[0])
        selected_title = self.goal_selector.get()
        if selected_title in self.goal_map:
            return self.goal_map[selected_title]
        return None

    def get_selected_log_id(self):
        selected_items = self.history_log_table.selection()
        if selected_items:
            return int(selected_items[0])
        selected_title = self.log_selector.get()
        if selected_title in self.log_map:
            return self.log_map[selected_title]
        return None

    def on_goal_treeview_select(self, event):
        selected_items = self.history_goal_table.selection()
        if selected_items:
            goal_id = int(selected_items[0])
            goal = dbman.get_goal_by_id(goal_id)
            if goal:
                self.goal_selector.set(goal[1])

    def on_log_treeview_select(self, event):
        selected_items = self.history_log_table.selection()
        if selected_items:
            log_id = int(selected_items[0])
            log = dbman.get_log_details_by_id(log_id)
            if log:
                self.log_selector.set(log[1])
                self.log_content_view.delete("1.0", "end")
                self.log_content_view.insert("1.0", f"Title: {log[1]}\nDate: {log[3]}\nMood Score: {log[4]}/10\n\nContent:\n{log[2]}")

    def on_goal_combobox_select(self, event):
        title = self.goal_selector.get()
        if title in self.goal_map:
            goal_id = str(self.goal_map[title])
            if self.history_goal_table.exists(goal_id):
                self.history_goal_table.selection_set(goal_id)
                self.history_goal_table.see(goal_id)

    def on_log_combobox_select(self, event):
        title = self.log_selector.get()
        if title in self.log_map:
            log_id = self.log_map[title]
            str_log_id = str(log_id)
            if self.history_log_table.exists(str_log_id):
                self.history_log_table.selection_set(str_log_id)
                self.history_log_table.see(str_log_id)
            log = dbman.get_log_details_by_id(log_id)
            if log:
                self.log_content_view.delete("1.0", "end")
                self.log_content_view.insert("1.0", f"Title: {log[1]}\nDate: {log[3]}\nMood Score: {log[4]}/10\n\nContent:\n{log[2]}")

    def handle_update_goal(self):
        goal_id = self.get_selected_goal_id()
        if not goal_id:
            messagebox.showwarning("Warning", "Please select a goal to update.")
            return
        goal = dbman.get_goal_by_id(goal_id)
        if goal:
            GoalEditDialog(self.window, goal_id, goal[1], goal[2], self.on_crud_success)

    def handle_delete_goal(self):
        goal_id = self.get_selected_goal_id()
        if not goal_id:
            messagebox.showwarning("Warning", "Please select a goal to delete.")
            return
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this goal?"):
            dbman.delete_goal(goal_id)
            self.on_crud_success()
            messagebox.showinfo("Success", "Goal deleted successfully.")

    def handle_update_log(self):
        log_id = self.get_selected_log_id()
        if not log_id:
            messagebox.showwarning("Warning", "Please select a daily log to update.")
            return
        log = dbman.get_log_details_by_id(log_id)
        if log:
            LogEditDialog(self.window, log_id, log[1], log[2], log[4], self.on_crud_success)

    def handle_delete_log(self):
        log_id = self.get_selected_log_id()
        if not log_id:
            messagebox.showwarning("Warning", "Please select a daily log to delete.")
            return
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this log?"):
            dbman.delete_daily_log(log_id)
            self.log_content_view.delete("1.0", "end")
            self.on_crud_success()
            messagebox.showinfo("Success", "Daily log deleted successfully.")

    def on_crud_success(self):
        self.refresh_tab_4()
        self.refresh_tab_1()

        

    # Executes on tab change, used to call various helper scripts
    def handle_tab_change(self, event):
        selected_tab = self.notebook.tab(self.notebook.select(), 'text')
        match selected_tab:
            case "Log Progress":
                self.refresh_tab_2()

            case "Dashboard":
                self.refresh_tab_1()

            case "History":
                self.refresh_tab_4()

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

