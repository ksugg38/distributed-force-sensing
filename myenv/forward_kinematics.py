# Katie Sugg
# Summer 2024 WVU REU Robotics

import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt

# This version declares the joint positions/axes inside the function.
# Run main() in this file or import into another file to use.


def forward_k(thetas: list) -> np.ndarray:
    # Thetas
    th1 = thetas[0]
    th2 = thetas[1]
    th3 = thetas[2]

    # Joint positions
    q1 = np.array([0, 46.13, -25.16])
    q2 = np.array([0, 90.28, -1.46])
    q3 = np.array([0, 226.04, -103.86])
    q4 = np.array([0, 125.53, - 237.13])

    # Homogenous coordinates. 1 is scaling factor
    p1 = np.hstack((q1, 1))
    p2 = np.hstack((q2, 1))
    p3 = np.hstack((q3, 1))
    p4 = np.hstack((q4, 1))

    # Joint axes as unit vectors - rotational velocities?
    w1 = np.array([0, np.sin(np.deg2rad(37)), np.cos(np.deg2rad(37))])
    w2 = np.array([1, 0, 0])
    w3 = np.array([1, 0, 0])

    # Joint axes as unit vectors - rotational velocities?
    w1_neg = np.array([0, -np.sin(np.deg2rad(37)), -np.cos(np.deg2rad(37))])
    w2_neg = np.array([-1, 0, 0])
    w3_neg = np.array([-1, 0, 0])

    # Calculate cross product between negative joint axis and joint position
    # Calculates linear velocities
    v1 = np.cross(w1_neg, q1)
    v2 = np.cross(w2_neg, q2)
    v3 = np.cross(w3_neg, q3)

    # Combines linear and rotational velocities - twists
    xi1 = np.hstack((v1, w1))
    xi2 = np.hstack((v2, w2))
    xi3 = np.hstack((v3, w3))

    # Create Homogenous Transformation Matrices
    T1 = matrixlog(xi1, th1)
    T2 = matrixlog(xi2, th2)
    T3 = matrixlog(xi3, th3)

    # Joint and end-effector coordinates
    j1 = p1
    j2 = np.matmul(np.matmul(T1, T2), (np.array(p2).transpose()))
    j3 = np.matmul(np.matmul(np.matmul(T1, T2), T3), np.array(p3).transpose())
    j4 = np.matmul(np.matmul(np.matmul(T1, T2), T3), np.array(p4).transpose())

    # End-effector coordinate
    pfoot = np.array(j4)[0][:3]

    # Array with joint and end-effector coordinates
    j = [np.array(j1)[:3], np.array(j2)[0][:3], np.array(j3)[0][:3], pfoot]
    print(j)

    # Return end-effector coordinate
    return pfoot


def matrixlog(xi: list, th) -> np.matrix:
    v = xi[:3]
    w = xi[3:]
    # assume theta is in radians
    R = np.matrix([[(np.cos(th)+w[0]**2*(1-math.cos(th))),
                    (w[0]*w[1]*(1-math.cos(th))-w[2]*math.sin(th)),
                    (w[0]*w[2]*(1-math.cos(th))+w[1]*math.sin(th))],
                  [(w[0]*w[1]*(1-math.cos(th))+w[2]*math.sin(th)),
                   (math.cos(th)+w[1]**2*(1-math.cos(th))),
                   (w[1]*w[2]*(1-math.cos(th))-w[0]*math.sin(th))],
                  [(w[0]*w[2]*(1-math.cos(th))-w[1]*math.sin(th)),
                   (w[1]*w[2]*(1-math.cos(th))+w[0]*math.sin(th)),
                   (math.cos(th)+w[2]**2*(1-np.cos(th)))]]
                  )

    x = (np.matmul((np.identity(3)-R), (np.cross(w, v)))
         + np.matmul(np.outer(w, w), v.transpose()) * th).transpose()
    T = np.vstack((np.hstack((R, x)), [0, 0, 0, 1]))
    return T


# Run file with a joint angle csv to see forward kinematics
def main():
    df = pd.read_csv("thetas.csv", header=None)
    foot = np.zeros((3, 240))
    th = []
    num_of_columns = len(df.columns)
    i = 0
    for i in range(num_of_columns):
        th.append(df[i].tolist())

    th = np.array(th)

    for j in range(240):
        foot[:, j] = forward_k(th[j, :])

    data = foot

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


if __name__ == "__main__":
    main()
