import tkinter
from tkinter import ttk
import dbman, forms

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

window.mainloop()
