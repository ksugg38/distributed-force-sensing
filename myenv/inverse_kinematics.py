from forward_kinematics_lists import forward_k
# from forward_kinematics import forward_k
from scipy.optimize import fsolve
import numpy as np
import matplotlib.pyplot as plt


def inverse_k(joint_positions: list, joint_axes: list,
              array_of_coordinates: list):
    # Make sure array_of_coordinates is np array
    array_of_coordinates = np.array(array_of_coordinates)

    # Get number of coordinates
    num_coords = len(array_of_coordinates)

    # Initialize arrays to store results
    thetas = np.zeros((3, num_coords))
    recreated_path = np.zeros((3, num_coords))
    theta_guess = np.array([0, 0, 0])

    def funct(th, coords):
        return coords - forward_k(th, joint_positions, joint_axes)

    # Newton-Raphson Root Finding Method
    for j in range(num_coords):
        # Calculated inverse kinematics
        thetas[:, j] = fsolve(funct, theta_guess,
                              args=array_of_coordinates[j, :])

        # Calculate forward_k to check footpath off of calculated theta
        recreated_path[:, j] = forward_k(thetas[:, j],
                                         joint_positions, joint_axes)

        # Update theta guess
        theta_guess = thetas[:, j]

    # Read the CSV file into a DataFrame
    data = recreated_path
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

    return thetas
