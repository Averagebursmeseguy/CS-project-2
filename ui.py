import tkinter
from tkinter import ttk
import dbman, forms, visualizer

#This changes window width and height
frame_width = 1000
frame_height = 600

window = tkinter.Tk()
window.geometry(f"{frame_width}x{frame_height}")
window.title("CS habit tracker")

notebook = ttk.Notebook(window)
notebook.pack(pady = 10,padx=20, expand = True)
                
#Individual tab descriptions. Put your UI elements here
frame1 = ttk.Frame(notebook, width = frame_width, height = frame_height)
notebook.add(frame1, text="Dashboard")


frame2 = ttk.Frame(notebook, width=frame_width, height=frame_height)
notebook.add(frame2, text="Log Progress")
log_form = forms.DailyLog(frame2)


frame3 = ttk.Frame(notebook, width=frame_width, height=frame_height)
notebook.add(frame3, text="Create Habit")
habit_form = forms.HabitForm(frame3)


frame4 = ttk.Frame(notebook, width=frame_width, height=frame_height)
notebook.add(frame4, text="History")

def refresh_tab_1():
    #updates the dashboard graphics and whatnot
    moods = dbman.fetch_column("daily_logs", "mood_score")
    
    mood_graph = visualizer.WellnessVisualizer(frame1)
    mood_graph.draw_mood_trend([1, 2, 3, 4, 5, 6],moods)

def refresh_tab_2():
    # dynamically changes habit log dropdown options.
    hobbies = dbman.fetch_unique('title', 'habits', True)
    log_form.habit_to_log_entry.config(values=hobbies) #this is a temporary measure. TODO: Fix later so that it returns actual list

    #TODO: Dynamically change unit context with selected habit

#Executes on tab change, used to call various helper scripts
def handle_tab_change(event):
    selected_tab = notebook.tab(notebook.select(), 'text')
    match selected_tab:
        case "Log Progress":
            refresh_tab_2()

        case "Dashboard":
            refresh_tab_1()

notebook.bind("<<NotebookTabChanged>>", handle_tab_change)



window.mainloop()



