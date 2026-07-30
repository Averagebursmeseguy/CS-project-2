import tkinter
from tkinter import ttk
import dbman, forms, visualizer

def createLoginWindow():
    loginWindow = tkinter.Tk()
    loginWindow.geometry("800x600")
    window.title("Login or sign up")

logged_in_user_id = 1
frame_width = 1000
frame_height = 600

window = tkinter.Tk()
window.geometry(f"{frame_width}x{frame_height}")
window.title("CS habit tracker")

notebook = ttk.Notebook(window)
notebook.pack(fill = 'both', expand=True)
                
# Individual tab descriptions. Put your UI elements here
frame1 = ttk.Frame(notebook, width=frame_width, height=frame_height)
current_goal_indicator = ttk.Label(text="no goals running", font=forms.font, master=frame1)
current_goal_indicator.pack()
non_qualitatives_table = ttk.Treeview(master = frame1, columns=("Habit done", "Times done"), show="headings")

notebook.add(frame1, text="Dashboard")

# Visualizer instance embedded in Dashboard (frame1)
mood_graph = visualizer.WellnessVisualizer(frame1)


frame2 = ttk.Frame(notebook, width=frame_width, height=frame_height)
notebook.add(frame2, text="Log Progress")
log_form = forms.DailyLog(frame2, 1)


frame3 = ttk.Frame(notebook, width=frame_width, height=frame_height)
notebook.add(frame3, text="Create Habit")
habit_form = forms.HabitForm(frame3, current_user=logged_in_user_id)


frame4 = ttk.Frame(notebook, width=frame_width, height=frame_height)
notebook.add(frame4, text="History")


def refresh_tab_1():
    # Updates the dashboard graphics and total goals count
    moods = dbman.fetch_column_by_user("daily_logs", "mood_score", logged_in_user_id)
    days = dbman.fetch_column_by_user('daily_logs', 'date_created', logged_in_user_id)

    if non_qualitatives_table.get_children() != ():
        for item in non_qualitatives_table.get_children():
            non_qualitatives_table.delete(item)
    else:
        pass

    for habit in dbman.get_count_non_qualitative_habits_user(logged_in_user_id):
        non_qualitatives_table.insert("", "end", values=habit)
    non_qualitatives_table.pack()

    goals_being_done = dbman.count_columns_by_user('goal_id','goals', logged_in_user_id)
    current_goal_indicator.config(text=f'''{goals_being_done} goals total, {dbman.get_finished_tasks_user(logged_in_user_id)} done, {dbman.get_pending_tasks_user(logged_in_user_id)} pending, {dbman.get_in_progress_tasks_user(logged_in_user_id)} tasks in progress.''')
    
    mood_graph.draw_mood_trend(days, moods, 'mood graph')
    mood_graph.draw_habit_progress(dbman.get_total_habit_prgresses_with_unit_by_user(logged_in_user_id
    ))


def refresh_tab_2():
    # Dynamically changes habit log dropdown options.
    hobbies = dbman.fetch_unique('title', 'habits', True)
    log_form.habit_to_log_entry.config(values=hobbies) 


# Executes on tab change, used to call various helper scripts
def handle_tab_change(event):
    selected_tab = notebook.tab(notebook.select(), 'text')
    match selected_tab:
        case "Log Progress":
            refresh_tab_2()

        case "Dashboard":
            refresh_tab_1()


notebook.bind("<<NotebookTabChanged>>", handle_tab_change)

window.mainloop()
