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

        self.save_coordinates_button = tk.Button(master,
                                                 text="Save Coordinates",
                                                 command=self.save_coordinates)
        # "Packs" button into tk window
        self.save_coordinates_button.pack()

    # maybe try to make an unclick, where it will take away a point

    def onclick(self, event):
        x = event.xdata
        z = event.ydata
        y = 0
        # Add point to graph
        if x is not None and z is not None:
            # You cand append as x, y, z. Then give an option to change the y
            self.points.append((x, y, z))
            self.axes.plot(x, z, 'ro')
            self.canvas.draw()

    def clear_points(self):
        self.points = []
        self.axes.clear()
        self.style()
        self.canvas.draw()

    def create_footpath(self):
        # Clear existing plot and reset style
        self.axes.clear()
        self.style()

        # Create bezier curve
        curve_points = self.create_bezier_curve()

        # Plot curve
        # self.axes.plot(curve_points[:, 0], curve_points[:, 1],
        #                '-o', label='Bezier Curve')

        # # Plot control points in red
        # self.axes.plot(input_array[:, 0], input_array[:, 1],
        #                'ro-', label='Control Points')

        # self.style()
        # self.axes.legend()

        # # Redraw canvas
        # self.canvas.draw()

        # Create a 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Extract x, y, z coordinates for plotting
        x, y, z = zip(*curve_points)

        # Plot curve_points on 3D plot
        ax.plot(x, y, z)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Show plot
        plt.show()

    def save_coordinates(self):
        # Create bezier curve
        curve_points = self.create_bezier_curve()

        # Save ouput to csv file
        np.savetxt("coordinates2.csv", curve_points,
                   delimiter=",")

    # Helper style function
    def style(self):
        # Style attributes
        self.axes.grid(True)
        self.axes.set_xlabel('X')
        self.axes.set_ylabel('Z')
        self.axes.set_xlim(0, 10)
        self.axes.set_ylim(0, 10)

    # Helper function
    def create_bezier_curve(self):
        input_array = np.array(self.points)
        if len(input_array) < 2:
            print("Need at least two points to draw a Bezier curve.")
            return
        # Create BezierSegment object
        bezier_segment = BezierSegment(input_array)

        # Create evenly distributed points
        t_values = np.linspace(0, 1, 100)

        # Create points along bezier segment
        curve_points = bezier_segment(t_values)
        return curve_points


def main():
    root = tk.Tk()
    # Wrapping it
    PointPlotter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
