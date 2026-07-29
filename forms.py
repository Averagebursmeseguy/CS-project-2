import tkinter
from tkinter import ttk
import dbman

# Standard font setup
font = ("Serif", 15)


class HabitForm():
    def __init__(self, master, current_user) -> None:
        self.master = master
        self.current_user = current_user

        # Variable to track the Checkbutton status (True = Checked, False = Unchecked)
        self.is_quant_var = tkinter.BooleanVar()

        # --- UI WIDGETS ---
        # Title
        self.title_label = ttk.Label(master=self.master, text="Title", font=font)
        self.title_input = ttk.Entry(font=font, master=self.master)

        # Quantitative Checkbox
        self.quant_label = ttk.Label(text="Quantitative", font=font, master=self.master)
        self.quant_selector = ttk.Checkbutton(master=self.master, variable=self.is_quant_var)

        # Unit
        self.unit_label = ttk.Label(text="Unit (if applicable)", font=font, master=self.master)
        self.unit_input = ttk.Entry(font=font, master=self.master)

        # Timespan Dropdown
        self.timespan_label = ttk.Label(text="Timespan", font=font, master=self.master)
        self.timespan_input = ttk.Combobox(
            master=self.master,
            values=['daily', 'weekly', 'monthly', 'yearly']
        )

        # Submit Button
        self.submit_btn = ttk.Button(
            master=self.master, 
            text="Submit Habit", 
            command=self.get_habit_data
        )

        # --- GRID LAYOUT ---
        self.title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.title_input.grid(row=0, column=1, padx=10, pady=10)

        self.quant_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.quant_selector.grid(row=1, column=1, padx=10, pady=10)

        self.unit_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.unit_input.grid(row=2, column=1, padx=10, pady=10)

        self.timespan_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.timespan_input.grid(row=3, column=1, padx=10, pady=10)

        self.submit_btn.grid(row=4, column=1, padx=10, pady=10)

    def get_habit_data(self):
        """Extracts data from the habit form as a list when the submit button is clicked."""
        title = self.title_input.get()
        if self.is_quant_var.get() == True:
            is_quant = 'true' 
        else:
            is_quant = 'false'

        if self.unit_input.get() != "":
            unit = self.unit_input.get()
        else:
            unit = None
        timespan = self.timespan_input.get()

        dbman.create_new_habit(self.current_user, title, is_quant, unit, timespan)



class DailyLog():
    def __init__(self, master) -> None:
        self.master = master
        
        # --- MOOD LOG FRAME (Right Side) ---
        self.mood_log_frame = ttk.Frame(master=self.master)

        self.title_label = ttk.Label(text="Title", font=font, master=self.mood_log_frame)
        self.title_entry = ttk.Entry(font=font, master=self.mood_log_frame)

        self.content_label = ttk.Label(text="Content", font=font, master=self.mood_log_frame)
        self.content_entry = tkinter.Text(master=self.mood_log_frame, height=10, width=40)

        self.mood_label = ttk.Label(text="Mood (1 - 10)", font=font, master=self.mood_log_frame)
        self.mood_scale = ttk.Scale(master=self.mood_log_frame, from_=1, to=10)

        self.submit_mood_button = ttk.Button(
            master=self.mood_log_frame, 
            text="Submit Mood", 
            command=self.get_mood_data
        )

        # Mood Log Grid
        self.title_label.grid(row=0, column=0, padx=3, pady=10, sticky="w")
        self.title_entry.grid(row=0, column=1, padx=3, pady=10, sticky="ew")
        
        self.content_label.grid(row=1, column=0, padx=3, pady=10, sticky="nw")
        self.content_entry.grid(row=1, column=1, padx=3, pady=10)
        
        self.mood_label.grid(row=2, column=0, padx=3, pady=10, sticky="w")
        self.mood_scale.grid(row=2, column=1, padx=3, pady=10, sticky="ew")
        
        self.submit_mood_button.grid(row=3, column=1, pady=10)


        # --- HABIT PROGRESS FRAME (Left Side) ---
        self.habit_progress_frame = ttk.Frame(master=self.master)

        self.habit_to_log_label = ttk.Label(text="Habit progress to log", font=font, master=self.habit_progress_frame)
        self.habit_to_log_entry = ttk.Combobox(values=['a', 'b', 'v'], master=self.habit_progress_frame)

        self.progress_log_label = ttk.Label(text="Dynamically generated.", font=font, master=self.habit_progress_frame)
        self.progress_entry = ttk.Entry(master=self.habit_progress_frame)
        self.progress_unit_label = ttk.Label(text=" ", font=font, master=self.habit_progress_frame)

        self.submitButton = ttk.Button(
            master=self.habit_progress_frame, 
            text="Submit Progress", 
            command=self.get_habit_progress_data
        )

        # Habit Progress Grid
        self.habit_to_log_label.grid(row=0, column=0)
        self.habit_to_log_entry.grid(row=0, column=1)
        self.progress_unit_label.grid(row=0, column=2)
        
        self.progress_log_label.grid(row=1, column=0)
        self.progress_entry.grid(row=1, column=1)
        
        self.submitButton.grid(row=4, column=1, pady=10)

        # Main Layout Placement (Frames side-by-side)
        self.habit_progress_frame.grid(row=0, column=0, padx=20)
        self.mood_log_frame.grid(row=0, column=1, padx=20)

    def get_mood_data(self):
        """Extracts data from the Mood Log section as a list."""
        title = self.title_entry.get()
        content = self.content_entry.get("1.0", "end-1c")
        mood_score = round(self.mood_scale.get())

        data_list = [title, content, mood_score]
        print("Collected Mood Log:", data_list)
        return data_list

    def get_habit_progress_data(self):
        """Extracts data from the Habit Progress section as a list."""
        selected_habit = self.habit_to_log_entry.get()
        progress_val = self.progress_entry.get()

        data_list = [selected_habit, progress_val]
        print("Collected Habit Progress:", data_list)
        return data_list
