import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# class WellnessVisualizer:
#     def __init__(self, parent_frame):
#         """
#         parent_frame: The Tkinter Frame widget where the graph will be embedded.
#         """
#         self.parent = parent_frame

#     def draw_mood_trend(self, days, mood_scores):
#         """
#         Generates a line plot of weekly mood scores and renders it inside the Tkinter frame.
#         """
#         # 1. Create a Matplotlib figure and axis
#         fig, ax = plt.subplots(figsize=(6, 3.5), dpi=100)
        
#         # 2. Build the mood trend chart
#         ax.plot(days, mood_scores, marker='o', color='#8854d0', linewidth=2.5)
#         ax.set_title('Weekly Mood Tracking Trend', fontsize=11, fontweight='bold')
#         ax.set_xlabel('Day')
#         ax.set_ylabel('Mood Score (1-10)')
#         ax.set_ylim(1, 10)
#         ax.grid(axis='y', linestyle='--', alpha=0.5)
        
#         plt.tight_layout()

#         # 3. Embed the plot inside the Tkinter parent frame
#         canvas = FigureCanvasTkAgg(fig, master=self.parent)
#         canvas_widget = canvas.get_tk_widget()
#         canvas_widget.pack(fill='both', expand=True)
#         canvas.draw()
        
#         return canvas_widget

x = [1, 2, 3, 5]
y = [9, 10, 11, 12]

plt.plot(x, y)

plt.show()

