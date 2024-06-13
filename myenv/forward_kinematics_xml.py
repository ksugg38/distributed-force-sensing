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
        neg = [k * -1 for k in joint_axes[j]]
        neg_joint_axes.append(neg)

    # Calculate cross product between negative joint axis and joint position
    # Calculates linear velocities
    linear_velocities = []
    for i in range(len(neg_joint_axes)):
        lv = np.cross(neg_joint_axes[i], joint_positions[i])
        linear_velocities.append(lv)

    # Combines linear and rotational velocities - twists
    twists = []
    for m in range(len(linear_velocities)):
        twist = np.concatenate(
            (linear_velocities[m], joint_axes[m]), axis=None)
        twists.append(twist)

    # Create Homogenous Transformation Matrices
    HTM = []
    for n in range(len(twists)):
        htm = matrixlog(twists[n], thetas[n])
        HTM.append(htm)

    end_effector = np.array(
        homogenous_coordinates[len(homogenous_coordinates) - 1])

    result = np.dot(HTM[0], HTM[1])  # Initialize result with the dot product
    for i in HTM[2:]:  # Start from HTM[2] for the iteration
        result = np.dot(result, i)

    # Perform the final dot product
    end_effector = np.dot(result, end_effector.transpose())
    pfoot = np.array(end_effector)[0][:3]
    return pfoot


def matrixlog(xi: list, th: float):
    v = xi[:2]
    w = xi[3:]
    R = np.matrix([[((math.cos(th)**2)*(1-math.cos(th))),
                    (w[0]*w[1]*(1-math.cos(th))-w[2]*math.sin(th)),
                    (w[0]*w[2]*(1-math.cos(th))+w[1]*math.sin(th))],
                  [(w[0]*w[1]*(1-math.cos(th))+w[2]*math.sin(th)),
                   ((math.cos(th)+w[1]**2)*(1-math.cos(th))),
                   (w[1]*w[2]*(1-math.cos(th))-w[0]*math.sin(th))],
                  [(w[0]*w[2]*(1-math.cos(th))-w[1]*math.sin(th)),
                   (w[1]*w[2]*(1-math.cos(th))+w[0]*math.sin(th)),
                   ((math.cos(th)+w[2]**2)*(1-math.cos(th)))]]
                  )

    x = (np.dot((np.identity(3)-R), (np.cross(w, v)))
         + np.dot(w, w.transpose()) * th).transpose()
    T = np.vstack((np.hstack((R, x)), [0, 0, 0, 1]))
    return T


def main():
    print(forward_k([1, 2, 1]))


if __name__ == "__main__":
    main()
