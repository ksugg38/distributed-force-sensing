# Katie Sugg
# Summer 2024 WVU REU Robotic

import numpy as np
import math
from forward_kinematics_lists import forward_k
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull, Delaunay
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Class PointChecker is used in coordinates.py
# This class allows you to check if a coordinate point is inside
# a robot's range of motion
# Define the correct joint positions and axes within __init__


class PointChecker:

    def __init__(self) -> None:
        # Joint positions
        # Last position should be end-effector
        q1 = [0, 46.13, -25.16]
        q2 = [0, 90.28, -1.46]
        q3 = [0, 226.04, -103.86]
        q4 = [0, 125.53, - 237.13]
        joint_positions = [q1, q2, q3, q4]

        # Joint axes as unit vectors
        w1 = [0, -math.sin(37), -math.cos(37)]
        w2 = [1, 0, 0]
        w3 = [1, 0, 0]
        joint_axes = [w1, w2, w3]

        # Create array of 10 numbers between 0 and 2*pi
        th1 = np.linspace(0, 2*np.pi, 10)
        th2 = np.linspace(np.pi/2, 3*np.pi/2, 10)
        th3 = np.linspace(0, np.pi, 10)

        # Create vectors of 3 numbers of every combo of th1, th2, th3
        TH1, TH2, TH3 = np.meshgrid(th1, th2, th3, indexing='ij')

        # Combine the grid arrays into a single array
        th_list = np.column_stack((TH1.ravel(), TH2.ravel(), TH3.ravel()))

        # Initalize coordinate array
        convex_hull_points = np.zeros((3, 1000))

        # Find the forward kinematic position using generated theta lis
        for i in range(1000):
            convex_hull_points[:, i] = forward_k(
                th_list[i, :], joint_positions, joint_axes)

        # Store points and convex hull in class attributes
        self.points = convex_hull_points
        self.hull = ConvexHull(convex_hull_points.T)

        # Create the Delaunay triangulation from the hull points
        self.delaunay = Delaunay(self.hull.points[self.hull.vertices])

    # This method graphs the point cloud
    def show_point_cloud(self) -> None:
        # Extract x, y, and z coordinates
        x = self.points[0]
        y = self.points[1]
        z = self.points[2]

        # Create a 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Plot the points
        ax.scatter(x, y, z)
        plt.show()

    # This method displays the convex hull
    def show_convex_hull(self) -> None:
        # Create a 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Plot the points
        # Uncomment line below to see convex hull with points
        ax.scatter(self.points[0], self.points[1], self.points[2])

        # Plot the convex hull
        for simplex in self.hull.simplices:
            vertices = self.points.T[simplex, :]
            ax.add_collection3d(Poly3DCollection(
                [vertices], facecolors='cyan', linewidths=1,
                edgecolors='r', alpha=.25))

        # Set plot limits
        ax.set_xlim([min(self.points[0]), max(self.points[0])])
        ax.set_ylim([min(self.points[1]), max(self.points[1])])
        ax.set_zlim([min(self.points[2]), max(self.points[2])])

        # Set plot labels
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        plt.show()

    # Function to check if a point is inside the convex hull
    def is_inside_hull(self, point) -> bool:
        return self.delaunay.find_simplex(point) >= 0


def main():
    pointss = PointChecker()
    pointss.show_convex_hull()
    # pointss.show_point_cloud()


if __name__ == "__main__":
    main()
