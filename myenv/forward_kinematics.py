import numpy as np
import math
import copy


def forward_k(thetas: list):
    # Thetas
    # For loop for x amount of thetas?
    th1 = thetas[0]
    th2 = thetas[1]
    th3 = thetas[2]

    # Joint positions
    # User edit corret positions
    # q0 = [0, 0, 0]
    q1 = [0, 46.13, -25.16]
    q2 = [0, 90.28, -1.46]
    q3 = [0, 226.04, -103.86]
    q4 = [0, 125.53, - 237.13]

    # Homogenous coordinates. 1 is scaling factor
    # automate for more positiions?
    p1 = copy.deepcopy(q1)
    p1.append(1)
    p2 = copy.deepcopy(q2)
    p2.append(1)
    p3 = copy.deepcopy(q3)
    p3.append(1)
    p4 = copy.deepcopy(q4)
    p4.append(1)

    # Joint axes as unit vectors - rotational velocities?
    w1 = [0, -math.sin(37), -math.cos(37)]
    w2 = [1, 0, 0]
    w3 = [1, 0, 0]

    w1_neg = [i * -1 for i in w1]
    w2_neg = [i * -1 for i in w2]
    w3_neg = [i * -1 for i in w3]

    # Calculate cross product between negative joint axis and joint position
    # Calculates linear velocities
    v1 = np.cross(w1_neg, q1)
    v2 = np.cross(w2_neg, q2)
    v3 = np.cross(w3_neg, q3)

    # Combines linear and rotational velocities - twists
    xi1 = np.concatenate((v1, w1), axis=None)
    xi2 = np.concatenate((v2, w2), axis=None)
    xi3 = np.concatenate((v3, w3), axis=None)

    # Create Homogenous Transformation Matrices
    T1 = matrixlog(xi1, th1)
    T2 = matrixlog(xi2, th2)
    T3 = matrixlog(xi3, th3)

    # j1 = p1
    # j2 = np.dot(np.dot(T1, T2), (np.array(p2).transpose()))
    # j3 = np.dot(np.dot(np.dot(T1, T2), T3), np.array(p3).transpose())
    j4 = np.dot(np.dot(np.dot(T1, T2), T3), np.array(p4).transpose())

    pfoot = np.array(j4)[0][:3]
    # j = [np.array(j1)[:3], np.array(j2)[0][:3], np.array(j3)[0][:3], pfoot]
    # print(j)
    # return j
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
