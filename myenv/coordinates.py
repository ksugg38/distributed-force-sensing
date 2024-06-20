import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.bezier import BezierSegment
import numpy as np


class PointPlotter:
    def __init__(self, master):
        self.master = master
        master.title("Footpath Generator")

        # Initialize graph
        self.figure, self.axes = plt.subplots(figsize=(5, 5))
        self.style_2d()
        self.axes.set_xlim(0, 100)
        self.axes.set_ylim(0, 100)
        self.points = []

        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas.draw()
        # Gets tk widget representing the Matplotlib canvas and "packs"
        # it into tk window, letting Matplotlib figure to be displayed
        # in the GUI app
        self.canvas.get_tk_widget().pack()

        self.click_cid = self.canvas.mpl_connect(
            'button_press_event', self.onclick)

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

    def onclick(self, event):
        x = round(event.xdata, 5)
        z = round(event.ydata, 5)
        y = 0
        # Add point to graph
        if x is not None and z is not None:
            self.show_entry_popup(x, y, z)

    def show_entry_popup(self, x, y, z):
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

        def confirm():
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

    def clear_points(self):
        # Empty points
        self.points = []
        self.figure.clear()

        # Redraw 2D graph
        self.axes = self.figure.add_subplot(111)
        self.style_2d()
        self.canvas.draw()
        self.enable_onclick()

    def create_footpath(self):
        # Clear existing plot and reset style
        self.figure.clear()
        self.axes = self.figure.add_subplot(111, projection='3d')
        self.style_3d()

        # Create bezier curve
        curve_points = self.create_bezier_curve()

        # Plot 3D curve
        if curve_points is not None:
            x, y, z = zip(*curve_points)
            self.axes.plot(x, y, z, 'b-', label='Bezier Curve')
            self.axes.legend()
            self.canvas.draw()

        # Disable onclick
        self.disable_onclick()

    def save_coordinates(self):
        # Create bezier curve
        curve_points = self.create_bezier_curve()

        # Save ouput to csv file
        np.savetxt("coordinates2.csv", curve_points,
                   delimiter=",")

    # Helper style functions
    def style_2d(self):
        self.axes.grid(True)
        self.axes.set_xlabel('X')
        self.axes.set_ylabel('Z')
        self.axes.set_xlim(0, 100)
        self.axes.set_ylim(0, 100)

    def style_3d(self):
        self.axes.grid(True)
        self.axes.set_xlabel('X')
        self.axes.set_ylabel('Y')
        self.axes.set_zlabel('Z')
        self.axes.set_xlim(0, 100)
        self.axes.set_ylim(0, 20)
        self.axes.set_zlim(0, 100)

    # Creates bezier curve
    def create_bezier_curve(self) -> list:
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
        curve_points = np.round(curve_points, 8)
        return curve_points

    # Disables during 3D graph
    def disable_onclick(self):
        self.canvas.mpl_disconnect(self.click_cid)

    def enable_onclick(self):
        self.click_cid = self.canvas.mpl_connect(
            'button_press_event', self.onclick)


def main():
    root = tk.Tk()
    # Wrapping it
    PointPlotter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
