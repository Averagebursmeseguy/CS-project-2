import tkinter
import time
from tkinter import ttk, messagebox
import dbman

font = ("Serif", 12)

class HabitForm:
    def __init__(self, master, current_user) -> None:
        self.master = master
        self.current_user = current_user
        self.is_quant_var = tkinter.BooleanVar()

        # UI Components
        self.title_label = ttk.Label(master=self.master, text="Title", font=font)
        self.title_input = ttk.Entry(font=font, master=self.master)

        self.quant_label = ttk.Label(text="Quantitative", font=font, master=self.master)
        self.quant_selector = ttk.Checkbutton(master=self.master, variable=self.is_quant_var)

        self.unit_label = ttk.Label(text="Unit (if applicable)", font=font, master=self.master)
        self.unit_input = ttk.Entry(font=font, master=self.master)

        self.timespan_label = ttk.Label(text="Timespan", font=font, master=self.master)
        self.timespan_input = ttk.Combobox(
            master=self.master,
            state="readonly",
            values=['daily', 'weekly', 'monthly', 'yearly']
        )
        self.timespan_input.current(0)

        self.submit_btn = ttk.Button(
            master=self.master, 
            text="Submit Habit", 
            command=self.get_habit_data
        )

        # Layout Alignment
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
        title = self.title_input.get().strip()
        if not title:
            messagebox.showwarning("Validation Error", "Title cannot be left blank.")
            return

        is_quant = 'true' if self.is_quant_var.get() else 'false'
        unit = self.unit_input.get().strip() or None
        timespan = self.timespan_input.get()

        if is_quant == 'true' and not unit:
            messagebox.showwarning("Validation Error", "Quantitative habits require a unit specification.")
            return

        dbman.create_new_habit(self.current_user, title, is_quant, unit, timespan)
        messagebox.showinfo("Success", "New habit logged successfully!")
        
        # Reset form fields
        self.title_input.delete(0, 'end')
        self.unit_input.delete(0, 'end')
        self.is_quant_var.set(False)


class DailyLog:
    def __init__(self, master, current_user) -> None:
        self.master = master
        self.current_user = current_user

        # Habit Progress Frame
        self.habit_progress_frame = ttk.LabelFrame(master=self.master, text="Log Habit Progress")
        
        self.habit_to_log_label = ttk.Label(text="Select Habit", font=font, master=self.habit_progress_frame)
        self.habit_to_log_entry = ttk.Combobox(master=self.habit_progress_frame, state="readonly")

        self.progress_log_label = ttk.Label(text="Value", font=font, master=self.habit_progress_frame)
        self.progress_entry = ttk.Entry(master=self.habit_progress_frame)

        self.submit_progress_btn = ttk.Button(
            master=self.habit_progress_frame, 
            text="Submit Progress", 
            command=self.get_habit_progress_data
        )

        self.habit_to_log_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.habit_to_log_entry.grid(row=0, column=1, padx=5, pady=5)
        self.progress_log_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.progress_entry.grid(row=1, column=1, padx=5, pady=5)
        self.submit_progress_btn.grid(row=2, column=1, pady=10)

        # Mood Log Frame
        self.mood_log_frame = ttk.LabelFrame(master=self.master, text="Log Mood & Journal Entry")

        self.title_label = ttk.Label(text="Title", font=font, master=self.mood_log_frame)
        self.title_entry = ttk.Entry(font=font, master=self.mood_log_frame)

        self.content_label = ttk.Label(text="Content", font=font, master=self.mood_log_frame)
        self.content_entry = tkinter.Text(master=self.mood_log_frame, height=8, width=35)

        self.mood_label = ttk.Label(text="Mood (1 - 10)", font=font, master=self.mood_log_frame)
        self.mood_scale = ttk.Scale(master=self.mood_log_frame, from_=1, to=10)
        self.mood_scale.set(5)

        self.submit_mood_button = ttk.Button(
            master=self.mood_log_frame, 
            text="Submit Mood Log", 
            command=self.get_mood_data
        )

        self.title_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        self.content_label.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.content_entry.grid(row=1, column=1, padx=5, pady=5)
        self.mood_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.mood_scale.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.submit_mood_button.grid(row=3, column=1, pady=10)

        # Component Grid Positioning
        self.habit_progress_frame.grid(row=0, column=0, padx=20, pady=20, sticky="n")
        self.mood_log_frame.grid(row=0, column=1, padx=20, pady=20, sticky="n")

    def get_mood_data(self):
        title = self.title_entry.get().strip()
        content = self.content_entry.get("1.0", "end-1c").strip()
        mood_score = round(self.mood_scale.get())

        if not title or not content:
            messagebox.showwarning("Validation Error", "Title and content fields cannot be blank.")
            return

        dbman.create_new_daily_log(self.current_user, title, content, mood_score)
        messagebox.showinfo("Success", "Daily log recorded!")
        self.title_entry.delete(0, 'end')
        self.content_entry.delete("1.0", "end")

    def get_habit_progress_data(self):
        selected_habit = self.habit_to_log_entry.get()
        progress_val = self.progress_entry.get().strip()

        if not selected_habit:
            messagebox.showwarning("Validation Error", "Please select a habit to update.")
            return

<<<<<<< HEAD
        dbman.create_new_habit_progress(self.current_user, selected_habit, int(time.time()), progress_val)
        print("Collected Habit Progress:", data_list)
        return data_list

class GoalForm():
    def __init__(self, master, current_user) -> None:
        self.current_user = current_user
        self.title_label = ttk.Label(master=master, font=font, text='Title of goal')
        self.title_label.grid(row=0, column=0, padx=10, pady=10)

        self.title_entry = ttk.Entry(font=font, master=master)
        self.title_entry.grid(row=0, column=1, padx=10, pady=10)

        self.submit_goal_button = ttk.Button(master = master, text='Submit New Goal', command=self.get_goal_data)
        self.submit_goal_button.grid(row=1, column=0, padx = 10, pady=10)

    def get_goal_data(self):
        title = self.title_entry.get()
        state = 'Pending'
        set_by = self.current_user

        goal_list = [title, set_by, state]
        print('Created goal:', goal_list)
        dbman.create_new_goal(set_by, title, state)
=======
        val_to_submit = float(progress_val) if progress_val else None

        dbman.create_new_habit_progress(self.current_user, selected_habit, int(time.time()), val_to_submit)
        messagebox.showinfo("Success", "Progress recorded!")
        self.progress_entry.delete(0, 'end')
>>>>>>> 5deb177b613c2f297df8e2053d4a7f6e970d5009
