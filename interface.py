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
        hobbies = dbman.fetch_unique('title', 'habits', True)
        self.log_form.habit_to_log_entry.config(values=hobbies) 


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
