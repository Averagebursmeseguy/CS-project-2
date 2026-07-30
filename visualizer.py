import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class WellnessVisualizer:
    def __init__(self, parent_frame):
        """
        parent_frame: The Tkinter Frame widget where the graph will be embedded.
        """
        self.parent = parent_frame
        self.canvas_widget = None
        self.canvas_widget2 = None

    def draw_mood_trend(self, days, mood_scores, graph_title):
        """
        Generates a line plot of weekly mood scores and renders it inside the Tkinter frame.
        """

        #  Destroy previous plot if it already exists
        if self.canvas_widget:
            self.canvas_widget.destroy()

        # Create a Matplotlib figure and axis
        fig, ax = plt.subplots(figsize=(6, 3.5), dpi=100)
        
        #  Build the mood trend chart
        ax.plot(days, mood_scores, marker='o', color='#8854d0', linewidth=2.5)
        ax.set_title(graph_title, fontsize=11, fontweight='bold')
        ax.set_xlabel('Day')
        ax.set_ylabel('Mood Score (1-10)')
        ax.set_ylim(1, 10)
        ax.grid(axis='y', linestyle='--', alpha=0.5)
        
        plt.tight_layout()

        #  Embed the plot inside the Tkinter parent frame
        canvas = FigureCanvasTkAgg(fig, master=self.parent)
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(side='left', expand=True)
        canvas.draw()
        
        return self.canvas_widget

    def draw_habit_progress(self, raw_values, graph_title="Habit Total Progress"):
        """
        Generates a bar chart of habit progress totals and renders it inside the Tkinter frame.
        """

        habits = []
        progress_values = []

        #quick and dirty un-tupler for result parsing
        for value in raw_values:
            habits.append(f"{value[0]} ({value[2]})")
            progress_values.append(value[1])


        #  Destroy previous plot if it already exists
        if self.canvas_widget2:
            self.canvas_widget2.destroy()

        #  Create a Matplotlib figure and axis
        fig, ax = plt.subplots(figsize=(6, 3.5), dpi=100)
        
        #  Build the habit progress bar chart
        bars = ax.bar(habits, progress_values, color='#4C72B0', edgecolor='black')
        ax.set_title(graph_title, fontsize=11, fontweight='bold')
        ax.set_xlabel('Habit Name')
        ax.set_ylabel('Total Progress')
        ax.grid(axis='y', linestyle='--', alpha=0.5)

        # Add data labels on top of each bar
        for bar in bars:
            yval = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2, 
                yval + 0.1, 
                f'{yval}', 
                ha='center', 
                va='bottom', 
                fontsize=9
            )
        
        plt.tight_layout()

        # Embedes the plot inside the Tkinter parent frame
        canvas = FigureCanvasTkAgg(fig, master=self.parent)
        self.canvas_widget2 = canvas.get_tk_widget()
        self.canvas_widget2.pack(side = 'right', expand=True)
        canvas.draw()
        
        return self.canvas_widget2
