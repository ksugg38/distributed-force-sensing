# Katie Sugg
# Summer 2024 WVU REU Robotics

from forward_kinematics_lists import forward_k
import scipy.optimize as op
import numpy as np
import matplotlib.pyplot as plt
import math

# This method is used in kinematics_bridge.py


def inverse_k(joint_positions: list, joint_axes: list,
              array_of_coordinates: list) -> np.ndarray:
    # Make sure array_of_coordinates is np array
    array_of_coordinates = np.array(array_of_coordinates)

    # Get number of coordinates
    num_coords = len(array_of_coordinates)

    # Initialize arrays to store results
    thetas = np.zeros((3, num_coords))
    recreated_path = np.zeros((3, num_coords))
    theta_guess = np.array([0, 0, 0])

    # Constraint function
    def constraint(th, coords, joint_positions, joint_axes):
        return coords - forward_k(th, joint_positions, joint_axes)

    for j in range(num_coords):

        # Function to minimize
        def funct(x_new):
            if j == 0:
                return np.sum([(x_new - theta_guess)**2])
            else:
                return np.sum([(x_new - thetas[:, j-1])**2])

        # Constraint function and arguments
        constraints = {'type': 'eq', 'fun': constraint, 'args': (
            array_of_coordinates[j, :], joint_positions, joint_axes)}

        # Store result
        result = op.minimize(funct, theta_guess,
                             method='SLSQP', constraints=constraints)

        # Get the optimized theta values
        thetas[:, j] = result.x

        # Calculate forward_k to check footpath off of calculated theta
        vector = [2*math.pi, 2*math.pi, 2*math.pi]
        recreated_path[:, j] = forward_k(thetas[:, j]-vector,
                                         joint_positions, joint_axes)

        # Update theta guess
        theta_guess = thetas[:, j]

    # Read the CSV file into a DataFrame
    data = recreated_path

    # Extract x, y, and z coordinates
    x = data[0]
    y = data[1]
    z = data[2]

    # # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the points
    ax.scatter(x, y, z, 'b-')

    # # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Recreated footpath using inverse kinematic thetas')

    # If y-axis is extremely streached out, uncomment the line below
    # plt.axis('equal')

    # Plot the results
    plt.figure()
    plt.plot(thetas[0, :], label='Servo 1')
    plt.plot(thetas[1, :], label='Servo 2')
    plt.plot(thetas[2, :], label='Servo 3')
    plt.legend()
    plt.xlabel('Coordinates')
    plt.ylabel('Angle')
    plt.title('Joint Angles change over Footpath Points')
    plt.show()

    return thetas
