import tkinter
from tkinter import ttk, messagebox
import forms, dbman

# Dummy Visualizer context handler in case module missing locally
try:
    import visualizer
except ImportError:
    class VisualizerDummy:
        def __init__(self, master): pass
        def draw_mood_trend(self, days, moods, title): pass
        def draw_habit_progress(self, data): pass
    visualizer = type('module', (), {'WellnessVisualizer': VisualizerDummy})

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
        self.mood_scale.set(current_mood if current_mood is not None else 5)
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


class Interface:
    def __init__(self, user) -> None:       
        self.logged_in_user_id = user
        self.frame_width = 1200
        self.frame_height = 700

        self.window = tkinter.Tk()
        self.window.geometry(f"{self.frame_width}x{self.frame_height}")
        self.window.title("CS Habit Tracker")

        dbman.make_dest_data()

        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill='both', expand=True)

        # Tab 1: Dashboard
        self.frame1 = ttk.Frame(self.notebook, width=self.frame_width, height=self.frame_height)
        self.current_goal_indicator = ttk.Label(text="no goals running", font=forms.font, master=self.frame1)
        self.current_goal_indicator.grid(row=0, column=0, columnspan=2, pady=10)

        self.non_qualitatives_table = ttk.Treeview(master=self.frame1, columns=("Habit done", "Times done"), show="headings")
        self.non_qualitatives_table.heading("Habit done", text='Habit Done')
        self.non_qualitatives_table.heading('Times done', text="Times Completed")
        self.non_qualitatives_table.grid(row=1, column=1, padx=10, pady=10)

        self.goal_table = ttk.Treeview(master=self.frame1, columns=('Goals', 'Status'), show='headings')
        self.goal_table.heading('Goals', text='Goal Target')
        self.goal_table.heading('Status', text='Current Status')
        self.goal_table.grid(row=1, column=0, padx=10, pady=10)

        self.notebook.add(self.frame1, text="Dashboard")
        self.mood_graph = visualizer.WellnessVisualizer(self.frame1)

        # Tab 2: Log Progress
        self.frame2 = ttk.Frame(self.notebook, width=self.frame_width, height=self.frame_height)
        self.notebook.add(self.frame2, text="Log Progress")
        self.log_form = forms.DailyLog(self.frame2, self.logged_in_user_id)

        # Tab 3: Create Habit
        self.frame3 = ttk.Frame(self.notebook, width=self.frame_width, height=self.frame_height)
        self.notebook.add(self.frame3, text="Create Habit")
        self.habit_form = forms.HabitForm(self.frame3, current_user=self.logged_in_user_id)

        # Tab 4: History Management
        self.frame4 = ttk.Frame(self.notebook, width=self.frame_width, height=self.frame_height)
        self.notebook.add(self.frame4, text="History")

        self.history_tab_label = ttk.Label(master=self.frame4, font=('Serif', 16, 'bold'), text="Historical Analytics")
        self.history_tab_label.grid(row=0, column=0, columnspan=3, pady=10)

        self.history_goal_table = ttk.Treeview(master=self.frame4, columns=('Goals', 'Status'), show='headings')
        self.history_goal_table.heading('Goals', text='Goal')
        self.history_goal_table.heading('Status', text='Status')
        self.history_goal_table.grid(row=1, column=0, padx=10, pady=10)

        self.history_log_table = ttk.Treeview(master=self.frame4, columns=('1', '2'), show='headings')
        self.history_log_table.heading('1', text="Title")
        self.history_log_table.heading('2', text='Date Created')
        self.history_log_table.grid(row=1, column=2, padx=10, pady=10)

        self.goal_selector = ttk.Combobox(self.frame4, state="readonly", width=30)
        self.goal_selector.grid(row=2, column=0, pady=5)

        self.log_selector = ttk.Combobox(self.frame4, state="readonly", width=30)
        self.log_selector.grid(row=2, column=2, pady=5)

        self.log_content_view = tkinter.Text(self.frame4, width=45, height=10, wrap="word")
        self.log_content_view.grid(row=3, column=2, pady=5)

        self.goal_map = {}
        self.log_map = {}

        # Bindings
        self.history_goal_table.bind("<<TreeviewSelect>>", self.on_goal_treeview_select)
        self.history_log_table.bind("<<TreeviewSelect>>", self.on_log_treeview_select)
        self.goal_selector.bind("<<ComboboxSelected>>", self.on_goal_combobox_select)
        self.log_selector.bind("<<ComboboxSelected>>", self.on_log_combobox_select)

        # Action Buttons
        self.goal_update_button = ttk.Button(self.frame4, text="Update Goal", command=self.handle_update_goal)
        self.goal_update_button.grid(row=3, column=0, pady=5)

        self.goal_delete_button = ttk.Button(self.frame4, text="Delete Goal", command=self.handle_delete_goal)
        self.goal_delete_button.grid(row=4, column=0, pady=5)

        self.log_update_button = ttk.Button(self.frame4, text="Update Log", command=self.handle_update_log)
        self.log_update_button.grid(row=4, column=2, pady=5)

        self.log_delete_button = ttk.Button(self.frame4, text="Delete Log", command=self.handle_delete_log)
        self.log_delete_button.grid(row=5, column=2, pady=5)

        self.notebook.bind("<<NotebookTabChanged>>", self.handle_tab_change)
        
        # Initial draw pass
        self.refresh_tab_1()
        self.window.mainloop()

    def handle_tab_change(self, event):
        selected_index = self.notebook.index(self.notebook.select())
        if selected_index == 0:
            self.refresh_tab_1()
        elif selected_index == 1:
            self.refresh_tab_2()
        elif selected_index == 3:
            self.refresh_tab_4()

    def refresh_tab_1(self):
        moods = dbman.fetch_column_by_user("daily_logs", "mood_score", self.logged_in_user_id)
        days = dbman.fetch_column_by_user('daily_logs', 'date_created', self.logged_in_user_id)

        for item in self.non_qualitatives_table.get_children():
            self.non_qualitatives_table.delete(item)

        for habit in dbman.get_count_non_qualitative_habits_user(self.logged_in_user_id):
            self.non_qualitatives_table.insert("", "end", values=habit)

        for item in self.goal_table.get_children():
            self.goal_table.delete(item)

        for goal in dbman.get_goals_by_user(self.logged_in_user_id):
            self.goal_table.insert("", "end", values=goal)
        
        goals_being_done = dbman.count_columns_by_user('goal_id', 'goals', self.logged_in_user_id)
        self.current_goal_indicator.config(
            text=f"{goals_being_done} Total Goals | {dbman.get_finished_tasks_user(self.logged_in_user_id)} Completed | "
                 f"{dbman.get_pending_tasks_user(self.logged_in_user_id)} Pending | {dbman.get_in_progress_tasks_user(self.logged_in_user_id)} Active"
        )
        
        self.mood_graph.draw_mood_trend(days, moods, 'Mood Tracking Trend')
        self.mood_graph.draw_habit_progress(dbman.get_total_habit_prgresses_with_unit_by_user(self.logged_in_user_id))

    def refresh_tab_2(self):
        hobbies = dbman.fetch_unique('title', self.logged_in_user_id, 'habits', True)
        self.log_form.habit_to_log_entry.config(values=hobbies)

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

    # Context Select Handlers
    def on_goal_treeview_select(self, event):
        selected = self.history_goal_table.selection()
        if selected:
            goal_id = selected[0]
            record = dbman.get_goal_by_id(goal_id)
            if record:
                self.goal_selector.set(record[1])

    def on_log_treeview_select(self, event):
        selected = self.history_log_table.selection()
        if selected:
            log_id = selected[0]
            record = dbman.get_log_details_by_id(log_id)
            if record:
                self.log_selector.set(record[1])
                self.log_content_view.delete("1.0", "end")
                self.log_content_view.insert("1.0", f"Mood: {record[4]}\n\n{record[2]}")

    def on_goal_combobox_select(self, event):
        title = self.goal_selector.get()
        if title in self.goal_map:
            goal_id = str(self.goal_map[title])
            self.history_goal_table.selection_set(goal_id)

    def on_log_combobox_select(self, event):
        title = self.log_selector.get()
        if title in self.log_map:
            log_id = str(self.log_map[title])
            self.history_log_table.selection_set(log_id)
            record = dbman.get_log_details_by_id(log_id)
            if record:
                self.log_content_view.delete("1.0", "end")
                self.log_content_view.insert("1.0", f"Mood: {record[4]}\n\n{record[2]}")

    # Operations Execution Routines
    def handle_update_goal(self):
        selected = self.history_goal_table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a goal to update.")
            return
        goal_id = selected[0]
        record = dbman.get_goal_by_id(goal_id)
        if record:
            GoalEditDialog(self.window, goal_id, record[1], record[2], self.refresh_tab_4)

    def handle_delete_goal(self):
        selected = self.history_goal_table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a goal to remove.")
            return
        goal_id = selected[0]
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this goal?"):
            dbman.delete_goal(goal_id)
            self.refresh_tab_4()

    def handle_update_log(self):
        selected = self.history_log_table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a log entry to update.")
            return
        log_id = selected[0]
        record = dbman.get_log_details_by_id(log_id)
        if record:
            LogEditDialog(self.window, log_id, record[1], record[2], record[4], self.refresh_tab_4)

    def handle_delete_log(self):
        selected = self.history_log_table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a log entry to delete.")
            return
        log_id = selected[0]
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this log entry?"):
            dbman.delete_daily_log(log_id)
            self.refresh_tab_4()


if __name__ == "__main__":
    # Test application execution entrypoint targeting user ID 1
    Interface(user=1)
