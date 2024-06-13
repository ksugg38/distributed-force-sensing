import pandas as pd
from forward_kinematics_xml import forward_k
from scipy.optimize import fsolve
import math
import numpy as np

# Make Pandas dataframe
# Change CSV name to correct file/file path
csv = "data3.csv"
df = pd.read_csv(csv, header=None)


# Get first df column and check if length is greater than 3
column_len = len(df[0].tolist())
if (column_len == 0 | column_len == 1):
    print("Please use correctly formatted coordinates data")
elif (column_len > 3):
    # Case 2: Columns are x,y,z - transpose df
    df = df.transpose()

# Case 1: Columns are coordinates
# Convert points to list and add to list
array_of_coordinates = []
num_of_columns = len(df.columns)
i = 0
for i in range(num_of_columns):
    array_of_coordinates.append(df[i].tolist())


# Define variables
swing_seconds = 2
stance_seconds = 2
step_time = swing_seconds + stance_seconds
num_steps = len(array_of_coordinates)
dt = step_time/num_steps

# Newton-Raphson Root Finding Method

# Joint positions
# Last position should be end-effector
q1 = [0, 46.13, -25.16]
q2 = [0, 90.28, -1.46]
q3 = [0, 226.04, -103.86]
q4 = [0, 125.53, - 237.13]
joint_positions = [q1, q2, q3, q4]

# Joint axes as unit vectors - rotational velocities?
w1 = [0, -math.sin(37), -math.cos(37)]
w2 = [1, 0, 0]
w3 = [1, 0, 0]
joint_axes = [w1, w2, w3]

# Initialize arrays to store results
th = np.zeros((3, num_steps))
foot = np.zeros((3, num_steps))
th_guess = np.array([0, 0, 0])
array_of_coordinates = np.array(array_of_coordinates)


def funct(th, coords): return coords - \
    forward_k(th, joint_positions, joint_axes)


for j in range(num_steps):
    th[:, j] = fsolve(lambda th: funct(
        th, array_of_coordinates[j]), th_guess)
    foot[:, j] = forward_k(th[:, j], joint_positions, joint_axes)
    th_guess = th[:, j]

print(th)
