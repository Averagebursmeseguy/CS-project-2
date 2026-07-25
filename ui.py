import tkinter
from tkinter import ttk

frame_width = 800
frame_height = 600

window = tkinter.Tk()
window.geometry(f"{frame_width}x{frame_height}")
window.title("CS habit tracker")

notebook = ttk.Notebook(window)
notebook.pack(pady = 10, expand = True)

frame1 = ttk.Frame(notebook, width = frame_width, height = frame_height)
frame1.pack(fill="both", expand= True)
notebook.add(frame1, text="Dashboard")

frame2 = ttk.Frame(notebook, width=frame_width, height=frame_height)
frame2.pack(fill='both', expand=True)
notebook.add(frame2, text="Log Progress")

frame3 = ttk.Frame(notebook, width=frame_width, height=frame_height)
frame3.pack(fill="both", expand=True)
notebook.add(frame3, text="Create Habit")

frame4 = ttk.Frame(notebook, width=frame_width, height=frame_height)
frame4.pack(fill="both", expand=True)
notebook.add(frame4, text="History")

window.mainloop()