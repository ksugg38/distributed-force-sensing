# Katie Sugg
# Summer 2024 WVU REU Robotics

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.bezier import BezierSegment
import numpy as np
import pandas as pd


class PointPlotter:
    def __init__(self, master) -> None:
        self.master = master
        master.title("Footpath Generator")

        # Initialize graph
        self.figure, self.axes = plt.subplots(figsize=(5, 5))
        self.style_2d()
        self.axes.set_xlim(0, 50)
        self.axes.set_ylim(0, 20)
        self.points = []
        self.footpath = []

        # Draws graph
        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas.draw()
        # Gets tk widget representing the Matplotlib canvas and "packs"
        # it into tk window, letting Matplotlib figure to be displayed
        # in the GUI app
        self.canvas.get_tk_widget().pack()

        # Connects graph to onclick
        self.click_cid = self.canvas.mpl_connect(
            'button_press_event', self.onclick)

        # Create clear points button
        self.clear_button = tk.Button(master, text="Clear Points",
                                      command=self.clear_points)
        # "Packs" button into tk window
        self.clear_button.pack()

        # Create footpath button
        self.footpath_button = tk.Button(
            master, text="Create Footpath", command=self.create_footpath)

        # "Packs" button into tk window
        self.footpath_button.pack()

        # Create save coordinates button
        self.save_coordinates_button = tk.Button(master,
                                                 text="Save Coordinates",
                                                 command=self.save_coordinates)
        # "Packs" button into tk window
        self.save_coordinates_button.pack()

    # Function to click points on graph
    def onclick(self, event) -> None:
        x = round(event.xdata, 5)
        z = round(event.ydata, 5)
        y = 0
        # Add point to graph
        if x is not None and z is not None:
            self.show_entry_popup(x, y, z)

    # Confirm and plots points
    def show_entry_popup(self, x, y, z) -> None:
        # Creates confirmation window
        popup = tk.Toplevel(self.master)
        popup.title("Enter Point")

        # Labels and entries for x, y, z
        label_x = tk.Label(popup, text="X:")
        label_x.pack()
        entry_x = tk.Entry(popup)
        entry_x.pack()
        entry_x.insert(tk.END, str(x))

        label_y = tk.Label(popup, text="Y:")
        label_y.pack()
        entry_y = tk.Entry(popup)
        entry_y.pack()
        entry_y.insert(tk.END, str(y))

        label_z = tk.Label(popup, text="Z:")
        label_z.pack()
        entry_z = tk.Entry(popup)
        entry_z.pack()
        entry_z.insert(tk.END, str(z))

        def confirm() -> None:
            try:
                x = float(entry_x.get())
                y = float(entry_y.get())
                z = float(entry_z.get())
                self.points.append((x, y, z))
                self.axes.plot(x, z, 'ro')
                self.canvas.draw()
                popup.destroy()
            except ValueError:
                error_label.config(text="Confirm numbers for x, y, and z.")

        confirm_button = tk.Button(popup, text="Confirm", command=confirm)
        confirm_button.pack()

        error_label = tk.Label(popup, text="", fg="red")
        error_label.pack()

    # Clear points on the screen
    def clear_points(self) -> None:
        # Empty points
        self.points = []
        self.figure.clear()

        # Redraw 2D graph
        self.axes = self.figure.add_subplot(111)
        self.style_2d()
        self.canvas.draw()
        self.enable_onclick()

    # Plots Bézier curve
    def create_footpath(self) -> None:
        # Clear existing plot and reset style
        self.figure.clear()
        self.axes = self.figure.add_subplot(111, projection='3d')
        self.style_3d()

        # Create footpath
        self.create_bezier_curve()

        # Plot 3D curve
        if self.footpath is not None:
            x, y, z = zip(*self.footpath)
            self.axes.plot(x, y, z, 'b-', label='Bezier Curve')
            self.axes.legend()
            self.canvas.draw()

        # Disable onclick
        self.disable_onclick()

    # Save coordinates to csv
    def save_coordinates(self) -> None:
        # make sure you have the most up to date footpath
        self.create_bezier_curve()

        # Save footpath to dataframe
        df = pd.DataFrame(self.footpath).transpose()

        # Save csv
        df.to_csv("test_coords3.csv", index=False, header=None)

    # 2D style function
    def style_2d(self) -> None:
        self.axes.grid(True)
        self.axes.set_xlabel('X')
        self.axes.set_ylabel('Z')
        self.axes.set_xlim(0, 50)
        self.axes.set_ylim(0, 20)

    # 3D style function
    def style_3d(self) -> None:
        self.axes.grid(True)
        self.axes.set_xlabel('X')
        self.axes.set_ylabel('Y')
        self.axes.set_zlabel('Z')
        self.axes.set_xlim(0, 50)
        self.axes.set_ylim(0, 10)
        self.axes.set_zlim(0, 20)

    # Creates bezier curve
    # def create_bezier_curve(self) -> list:
    def create_bezier_curve(self):
        # Get list of points
        input_array = np.array(self.points)

        # Error checking
        if len(input_array) < 2:
            print("Need at least two points to draw a Bezier curve.")
            return

        # Create BezierSegment object
        bezier_segment = BezierSegment(input_array)

        # Create evenly distributed points
        t_values = np.linspace(0, 1, 150)

        # Create points along bezier segment and rounds
        curve_points = np.round(bezier_segment(t_values), 8)

        # Connects the ends of the curve in flipped order
        bottom_line = np.linspace(
            curve_points[len(curve_points)-1], curve_points[0], 90)

        # Get middle of curve
        mid_index = len(curve_points) // 2

        # Split curve into two pieces
        first_half = curve_points[:mid_index]
        second_half = curve_points[mid_index:]

        # Connect pieces to create footpath
        result = np.concatenate(
            (second_half, bottom_line, first_half), axis=0)
        self.footpath = result
        # return result

    # Disables during 3D graph
    def disable_onclick(self) -> None:
        self.canvas.mpl_disconnect(self.click_cid)

    # Enables clicking ability
    def enable_onclick(self) -> None:
        self.click_cid = self.canvas.mpl_connect(
            'button_press_event', self.onclick)


def main():
    root = tk.Tk()
    # Wrapping root in class
    PointPlotter(root)
    root.mainloop()


# Will automatically run main
if __name__ == "__main__":
    main()
