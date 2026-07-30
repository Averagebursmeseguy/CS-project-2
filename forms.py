import time
import tkinter
from tkinter import messagebox, ttk
import dbman

# Standard font setup
font = ("Serif", 15)


class GoalForm:
    def __init__(self, master, current_user) -> None:
        self.master = master
        self.current_user = current_user

        # --- UI WIDGETS ---
        # Title
        self.title_label = ttk.Label(
            master=self.master, text="Goal Title", font=font
        )
        self.title_input = ttk.Entry(font=font, master=self.master)

        # Status Dropdown
        self.status_label = ttk.Label(
            master=self.master, text="State", font=font
        )
        self.status_input = ttk.Combobox(
            master=self.master,
            values=["Pending", "In Progress", "Completed"],
            state="readonly",
        )
        self.status_input.set("Pending")

        # Select Existing Goal (for Update / Delete)
        self.select_label = ttk.Label(
            master=self.master, text="Select Existing Goal", font=font
        )
        self.goal_selector = ttk.Combobox(
            master=self.master, values=[], state="readonly"
        )

        # Buttons
        self.submit_btn = ttk.Button(
            master=self.master,
            text="Create Goal",
            command=self.create_goal_data,
        )

        self.update_btn = ttk.Button(
            master=self.master,
            text="Update Selected Goal",
            command=self.update_goal_data,
        )

        self.delete_btn = ttk.Button(
            master=self.master,
            text="Delete Selected Goal",
            command=self.delete_goal_data,
        )

        # --- GRID LAYOUT ---
        self.title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.title_input.grid(row=0, column=1, padx=10, pady=10)

        self.status_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.status_input.grid(row=1, column=1, padx=10, pady=10)

        self.submit_btn.grid(row=2, column=1, padx=10, pady=10)

        # Divider Section for Management
        self.select_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.goal_selector.grid(row=3, column=1, padx=10, pady=10)

        self.update_btn.grid(row=4, column=0, padx=10, pady=10)
        self.delete_btn.grid(row=4, column=1, padx=10, pady=10)

        self.refresh_goals_list()

    def refresh_goals_list(self):
        """Fetches active user goals to populate dropdown."""
        dbman.cursor.execute(
            "SELECT goal_id, title FROM goals WHERE set_by_id = ?",
            (self.current_user,),
        )
        self.goals_dict = {f"{row[1]} (ID: {row[0]})": row[0] for row in dbman.cursor.fetchall()}
        self.goal_selector["values"] = list(self.goals_dict.keys())

    def create_goal_data(self):
        """Creates a new goal."""
        title = self.title_input.get().strip()
        state = self.status_input.get()

        if title:
            dbman.create_new_goal(self.current_user, title, state)
            messagebox.showinfo("Success", "Goal created successfully!")
            self.refresh_goals_list()
            self.title_input.delete(0, "end")
        else:
            messagebox.showerror("Error", "Goal title cannot be empty.")

    def update_goal_data(self):
        """Updates selected goal's state and title."""
        selected_text = self.goal_selector.get()
        if not selected_text or selected_text not in self.goals_dict:
            messagebox.showwarning("Warning", "Please select a goal to update.")
            return

        goal_id = self.goals_dict[selected_text]
        new_title = self.title_input.get().strip()
        new_state = self.status_input.get()

        dbman.update_goal(
            goal_id,
            self.current_user,
            title=new_title if new_title else None,
            state=new_state,
        )
        messagebox.showinfo("Success", "Goal updated!")
        self.refresh_goals_list()

    def delete_goal_data(self):
        """Deletes selected goal from database."""
        selected_text = self.goal_selector.get()
        if not selected_text or selected_text not in self.goals_dict:
            messagebox.showwarning("Warning", "Please select a goal to delete.")
            return

        goal_id = self.goals_dict[selected_text]
        dbman.delete_goal(goal_id, self.current_user)
        messagebox.showinfo("Success", "Goal deleted!")
        self.refresh_goals_list()


class HabitForm:
    def __init__(self, master, current_user) -> None:
        self.master = master
        self.current_user = current_user

        # Variable to track the Checkbutton status (True = Checked, False = Unchecked)
        self.is_quant_var = tkinter.BooleanVar()

        # --- UI WIDGETS ---
        # Title
        self.title_label = ttk.Label(
            master=self.master, text="Title", font=font
        )
        self.title_input = ttk.Entry(font=font, master=self.master)

        # Quantitative Checkbox
        self.quant_label = ttk.Label(
            text="Quantitative", font=font, master=self.master
        )
        self.quant_selector = ttk.Checkbutton(
            master=self.master, variable=self.is_quant_var
        )

        # Unit
        self.unit_label = ttk.Label(
            text="Unit (if applicable)", font=font, master=self.master
        )
        self.unit_input = ttk.Entry(font=font, master=self.master)

        # Timespan Dropdown
        self.timespan_label = ttk.Label(
            text="Timespan", font=font, master=self.master
        )
        self.timespan_input = ttk.Combobox(
            master=self.master,
            values=["daily", "weekly", "monthly", "yearly"],
            state="readonly",
        )
        self.timespan_input.set("daily")

        # Existing Habit Selector for updates/deletions
        self.select_label = ttk.Label(
            master=self.master, text="Select Existing Habit", font=font
        )
        self.habit_selector = ttk.Combobox(
            master=self.master, values=[], state="readonly"
        )

        # Buttons
        self.submit_btn = ttk.Button(
            master=self.master,
            text="Submit Habit",
            command=self.get_habit_data,
        )

        self.delete_btn = ttk.Button(
            master=self.master,
            text="Delete Selected Habit",
            command=self.delete_habit_data,
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

        # Manage Section
        self.select_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.habit_selector.grid(row=5, column=1, padx=10, pady=10)

        self.delete_btn.grid(row=6, column=1, padx=10, pady=10)

        self.refresh_habits_list()

    def refresh_habits_list(self):
        """Fetches active habits to populate management dropdown."""
        dbman.cursor.execute(
            "SELECT habit_id, title FROM habits WHERE set_by_id = ?",
            (self.current_user,),
        )
        self.habits_dict = {
            f"{row[1]} (ID: {row[0]})": row[0] for row in dbman.cursor.fetchall()
        }
        self.habit_selector["values"] = list(self.habits_dict.keys())

    def get_habit_data(self):
        """Extracts data from the habit form and writes to DB."""
        title = self.title_input.get().strip()
        is_quant = "true" if self.is_quant_var.get() else "false"

        unit = self.unit_input.get().strip()
        if not unit:
            unit = None

        timespan = self.timespan_input.get()

        if title:
            dbman.create_new_habit(
                self.current_user, title, is_quant, unit, timespan
            )
            messagebox.showinfo("Success", "Habit added successfully!")
            self.refresh_habits_list()
        else:
            messagebox.showerror("Error", "Title cannot be empty")

    def delete_habit_data(self):
        """Deletes selected habit."""
        selected_text = self.habit_selector.get()
        if not selected_text or selected_text not in self.habits_dict:
            messagebox.showwarning(
                "Warning", "Please select a habit to delete."
            )
            return

        habit_id = self.habits_dict[selected_text]
        dbman.delete_habit(habit_id, self.current_user)
        messagebox.showinfo("Success", "Habit deleted!")
        self.refresh_habits_list()


class DailyLog:
    def __init__(self, master, current_user) -> None:
        self.master = master
        self.current_user = current_user

        # --- MOOD LOG FRAME (Right Side) ---
        self.mood_log_frame = ttk.Frame(master=self.master)

        self.title_label = ttk.Label(
            text="Title", font=font, master=self.mood_log_frame
        )
        self.title_entry = ttk.Entry(font=font, master=self.mood_log_frame)

        self.content_label = ttk.Label(
            text="Content", font=font, master=self.mood_log_frame
        )
        self.content_entry = tkinter.Text(
            master=self.mood_log_frame, height=10, width=40
        )

        self.mood_label = ttk.Label(
            text="Mood (1 - 10)", font=font, master=self.mood_log_frame
        )
        self.mood_scale = ttk.Scale(
            master=self.mood_log_frame, from_=1, to=10
        )

        self.submit_mood_button = ttk.Button(
            master=self.mood_log_frame,
            text="Submit Mood",
            command=self.get_mood_data,
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

        self.habit_to_log_label = ttk.Label(
            text="Habit progress to log",
            font=font,
            master=self.habit_progress_frame,
        )

        # Dynamic habit fetching
        user_habits = (
            dbman.fetch_unique("title", self.current_user, "habits", True) or []
        )

        self.habit_to_log_entry = ttk.Combobox(
            values=user_habits, master=self.habit_progress_frame
        )

        self.progress_log_label = ttk.Label(
            text="Quantity / Progress", font=font, master=self.habit_progress_frame
        )
        self.progress_entry = ttk.Entry(master=self.habit_progress_frame)
        self.progress_unit_label = ttk.Label(
            text=" ", font=font, master=self.habit_progress_frame
        )

        self.submitButton = ttk.Button(
            master=self.habit_progress_frame,
            text="Submit Progress",
            command=self.get_habit_progress_data,
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
        """Extracts data from the Mood Log section and submits to DB."""
        title = self.title_entry.get().strip()
        content = self.content_entry.get("1.0", "end-1c").strip()
        mood_score = round(self.mood_scale.get())

        if title and content:
            dbman.create_new_daily_log(
                self.current_user, title, content, mood_score
            )
            messagebox.showinfo("Success", "Daily log saved!")
            self.title_entry.delete(0, "end")
            self.content_entry.delete("1.0", "end")
        else:
            messagebox.showerror(
                "Error", "Log Title and Content cannot be empty."
            )

    def get_habit_progress_data(self):
        """Extracts data from the Habit Progress section and saves it."""
        selected_habit = self.habit_to_log_entry.get()
        progress_val = self.progress_entry.get()

        if selected_habit:
            current_timestamp = int(time.time())
            try:
                numeric_val = float(progress_val) if progress_val else None
            except ValueError:
                numeric_val = None

            dbman.create_new_habit_progress(
                self.current_user,
                selected_habit,
                current_timestamp,
                numeric_val,
            )
            messagebox.showinfo("Success", "Habit progress recorded!")
            self.progress_entry.delete(0, "end")
        else:
            messagebox.showerror("Error", "Please select a habit first.")
