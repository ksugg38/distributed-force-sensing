import numpy as np
import math
import copy


def forward_k(thetas: list, joint_positions: list, joint_axes: list):
    # Homogenous coordinates. 1 is scaling factor
    homogenous_coordinates = []
    for i in range(len(joint_positions)):
        p = copy.deepcopy(joint_positions[i])
        p.append(1)
        homogenous_coordinates.append(p)

    neg_joint_axes = []
    for j in range(len(joint_axes)):
        neg = copy.deepcopy(joint_axes[j])
        neg = [k * -1 for k in neg]
        neg_joint_axes.append(neg)

    # Calculate cross product between negative joint axis and joint position
    # Calculates linear velocities
    linear_velocities = []
    for i in range(len(neg_joint_axes)):
        lv = np.cross(neg_joint_axes[i], joint_positions[i])
        linear_velocities.append(lv)

    # Combines linear and rotational velocities - twists
    twists = []
    for i in range(len(linear_velocities)):
        twist = np.concatenate(
            (linear_velocities[i], joint_axes[i]), axis=None)
        twists.append(twist)

    # Create Homogenous Transformation Matrices
    HTM = []
    for i in range(len(twists)):
        htm = matrixlog(twists[i], thetas[i])
        HTM.append(htm)

    end_effector = np.array(
        homogenous_coordinates[len(homogenous_coordinates) - 1])

    result = np.matmul(HTM[0], HTM[1])  # Initialize result
    for i in HTM[2:]:  # Start from HTM[2] for the iteration
        result = np.matmul(result, i)

    # Perform the final matrix multiplication
    end_effector = np.matmul(result, end_effector.transpose())
    pfoot = np.array(end_effector)[0][:3]
    return pfoot


def matrixlog(xi: list, th: float):
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
