# Katie Sugg
# Summer 2024 WVU REU Robotics

import pandas as pd
from inverse_kinematics import inverse_k
import math
import matplotlib.pyplot as plt


# Change CSV name to correct file/file path
# csv = "revised_with_ratios2.csv"
# csv = "./myenv/coordinates.csv"
csv = "test_coords3.csv"

# Make Pandas dataframe
df = pd.read_csv(csv, header=None)


# Get first df column and check if length is greater than 3
column_len = len(df[0].tolist())
if (column_len == 0 | column_len == 1):
    raise Exception("Please use correctly formatted coordinates data")
elif (column_len > 3):
    # Case 2: Columns are x,y,z - transpose df
    df = df.transpose()
# print(df)

# Case 1: Columns are coordinates
# Convert points to list and add to array_of_coordinates
array_of_coordinates = []
num_of_columns = len(df.columns)
i = 0
for i in range(num_of_columns):
    array_of_coordinates.append(df[i].tolist())

# DEFINE EVERYTHING

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

df2 = pd.DataFrame(array_of_coordinates)
print(df2)

# Calculate joint angles
joint_angles = inverse_k(joint_positions, joint_axes, array_of_coordinates)

# Convert to pandas dataframe
df = pd.DataFrame(joint_angles)

x1 = df.loc[0]
y1 = df.loc[1]
z1 = df.loc[2]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(x1, y1, z1, c='r', marker='o', label='First Set')
plt.show()

# Save it to csv
df.to_csv("joint_angles2.csv", index=False, header=None)
