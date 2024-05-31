import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.bezier import BezierSegment
import numpy as np


class PointPlotter:
    def __init__(self, master):
        self.master = master
        master.title("Interactive Point Plotter")

        self.figure, self.axes = plt.subplots(figsize=(4, 4))
        self.style()
        self.axes.set_xlim(0, 10)
        self.axes.set_ylim(0, 10)
        self.points = []

        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas.draw()
        # Gets tk widget representing the Matplotlib canvas and "packs"
        # it into tk window, letting Matplotlib figure to be displayed
        # in the GUI app
        self.canvas.get_tk_widget().pack()

        self.canvas.mpl_connect('button_press_event', self.onclick)

        self.clear_button = tk.Button(master, text="Clear Points",
                                      command=self.clear_points)
        # "Packs" button into tk window
        self.clear_button.pack()

        self.footpath_button = tk.Button(
            master, text="Create Footpath", command=self.create_footpath)

        # "Packs" button into tk window
        self.footpath_button.pack()

    # maybe try to make an unclick, where it will take away a point

    def onclick(self, event):
        x = event.xdata
        y = event.ydata
        # Add point to graph
        if x is not None and y is not None:
            self.points.append((x, y))
            self.axes.plot(x, y, 'ro')
            self.canvas.draw()

    def clear_points(self):
        self.points = []
        self.axes.clear()
        self.style()
        self.canvas.draw()

    def create_footpath(self):
        # Convert to NumPy array - got issues otherwise
        input_array = np.array(self.points)
        if len(input_array) < 2:
            print("Need at least two points to draw a Bezier curve.")
            return

        # Clear existing plot and reset style
        self.axes.clear()
        self.style()

        # Create BezierSegment object
        bezier_segment = BezierSegment(input_array)

        # Create evenly distributed points
        t_values = np.linspace(0, 1, 100)

        # Create points along bezier segment
        curve_points = bezier_segment(t_values)

        # Plot curve
        self.axes.plot(curve_points[:, 0], curve_points[:, 1],
                       '-o', label='Bezier Curve')

        # Plot control points in red
        self.axes.plot(input_array[:, 0], input_array[:, 1],
                       'ro-', label='Control Points')

        self.style()
        self.axes.legend()

        # Redraw canvas
        self.canvas.draw()

    def style(self):
        # Style attributes
        self.axes.grid(True)
        self.axes.set_xlabel('X')
        self.axes.set_ylabel('Y')
        self.axes.set_xlim(0, 10)
        self.axes.set_ylim(0, 10)


def main():
    root = tk.Tk()
    # Wrapping it
    PointPlotter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
