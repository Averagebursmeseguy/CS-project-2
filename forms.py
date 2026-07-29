import tkinter
from tkinter import ttk
font = ("Serif", 15)

class HabitForm():
    def __init__(self, master) -> None:
        self.master = master

        #title
        self.title_label = ttk.Label(master=self.master, text="Title", font=font)
        self.title_input = ttk.Entry(font=font, master = self.master)

        #quant
        self.quant_label = ttk.Label(text="Quantitive",font=font, master = self.master)
        self.quant_selector = ttk.Checkbutton(master = self.master, width=10)

        #unit
        self.unit_label = ttk.Label(text="Unit(if applicable)", font=font, master = self.master)
        self.unit_input = ttk.Entry(font=font, master = self.master)

        #timespan
        self.timespan_label = ttk.Label(text="Timespan", font=font, master=self.master)
        self.timespan_input = ttk.Combobox(master=self.master,
                                      values=['daily', 'weekly', 'monthly', 'yearly'] 
                                      )


        #Grid(UGHHHHH)
        self.title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.title_input.grid(row=0, column=1, padx=10, pady=10)

        self.quant_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.quant_selector.grid(row=1, column=1, padx=10, pady=10)

        self.unit_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.unit_input.grid(row=2, column=1, padx=10, pady=10)

        self.timespan_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.timespan_input.grid(row=3, column=1, padx=10, pady=10)

    def doNothing(self, a, b):
        return

class DailyLog():
    def __init__(self, master) -> None:
        self.master = master
        self.mood_log_frame = ttk.Frame(master=self.master)

        #Title
        self.title_label = ttk.Label(text="Title", font=font, master=self.mood_log_frame)
        self.title_entry = ttk.Entry(font=font, master=self.mood_log_frame)

        #Content
        self.content_label = ttk.Label(text="Content", font = font, master = self.mood_log_frame)
        self.content_entry = tkinter.Text(master = self.mood_log_frame, height=20, width=40)

        #Mood Score
        self.mood_label = ttk.Label(text = "Mood(1 - 10)", font=font, master=self.mood_log_frame)
        self.mood_scale = ttk.Scale(master=self.mood_log_frame, from_=1, to=10)

        #Submit button
        self.submit_mood_button = ttk.Button(master = self.mood_log_frame, text="Submit")

        #This is getting kinda ridiculous
            
        self.title_label.grid(
        row=0,
        column=0,
        padx=3,
        pady=10,
        sticky="w"
    )
        self.title_entry.grid(
        row=0,
        column=1,
        padx=3,
        pady=10,
        sticky="ew"
    )
        self.content_label.grid(
        row=1,
        column=0,
        padx=3,
        pady=10,
        sticky="nw"
    )
        self.content_entry.grid(
        row=1,
        column=1,
        padx=3,
        pady=10
    )
        self.mood_label.grid(
        row=2,
        column=0,
        padx=3,
        pady=10,
        sticky="w"
    )
        self.mood_scale.grid(
        row=2,
        column=1,
        padx=3,
        pady=10,
        sticky="ew"
    )
        self.submit_mood_button.grid(
            row = 3, column=1
        )

    #You thought we were done?

        self.habit_progress_frame = ttk.Frame(master = self.master)

        self.habit_to_log_label = ttk.Label(text="Habit progress to log", font=font, master=self.habit_progress_frame)
        self.habit_to_log_entry = ttk.Combobox(values=['a', 'b', 'v'], master=self.habit_progress_frame)

        self.progress_log_label = ttk.Label(text = "Dynamically generated.", font=font, master=self.habit_progress_frame)
        self.progress_entry = ttk.Entry(master=self.habit_progress_frame)
        self.progress_unit_label = ttk.Label(text=" ", font=font, master=self.habit_progress_frame)

        self.submitButton = ttk.Button(master=self.habit_progress_frame, text="Submit")

        self.habit_to_log_label.grid(row=0, column=0)
        self.habit_to_log_entry.grid(row=0, column=1)
        self.progress_unit_label.grid(row=0, column=2)
        self.progress_log_label.grid(row=1, column=0)
        self.progress_entry.grid(row=1, column=1)
        self.submitButton.grid(row=4, column=1)

        self.habit_progress_frame.grid(
            row=0, column=0, padx=20
        )

        self.mood_log_frame.grid(
            row=0, column=1, padx=20
        )






        




    
        