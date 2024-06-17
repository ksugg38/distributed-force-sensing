# from forward_kinematics_lists import forward_k
from forward_kinematics import forward_k
from scipy.optimize import fsolve
import numpy as np
import matplotlib.pyplot as plt

# joint_positions: list, joint_axes: list,


def inverse_k(
        array_of_coordinates: list):

    num_steps = len(array_of_coordinates)

    # Newton-Raphson Root Finding Method
    # Initialize arrays to store results
    th = np.zeros((3, num_steps))
    # th = np.zeros((3, 1))
    foot = np.zeros((3, num_steps))
    th_guess = np.array([0, 0, 0])
    array_of_coordinates = np.array(array_of_coordinates)

    # fun = lambda th(th, coords): coords - forward_k(th)
    # forward_k(th, joint_positions, joint_axes)
    # funct = lambda th, coords: coords - forward_k(th)
    # lambda th, coords: coords - forward_k(th)

    # print(array_of_coordinates[1:3, :])

    def funct(th, coords):
        # print("coords")
        # print(coords)
        # print("th")
        # print(th)
        # print("after theta")
        return coords - forward_k(th)

    for j in range(num_steps):

        # k = j + 1
        array = array_of_coordinates[j, :]
        # print("array")
        # print(array)
        # print("after array")

        th[:, j] = fsolve(funct, th_guess, args=array)
        # print("th")
        # print(th[:, j])
        # print("array")
        # print(array)
        # th[:, j] = fsolve(array - theta, th_guess)
        # th[:, j] = fsolve(funct, th_guess, args=(array_of_coordinates[:, j],))
        # foot[:, j] = forward_k(th[:, j], joint_positions, joint_axes)
        foot[:, j] = forward_k(th[:, j])
        # th_guess = th[:, j]

    # Read the CSV file into a DataFrame
    data = foot
    print(data)

    # Extract x, y, and z coordinates
    x = data[0]
    y = data[1]
    z = data[2]

    # # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # # Plot the points
    ax.scatter(x, y, z)

    # # Set labels and title
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    ax.set_title('3D Scatter Plot')

    # # Show the plot
    plt.show()

    return th
