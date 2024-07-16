# Katie Sugg
# Summer 2024 WVU REU Robotics

import pandas as pd
import matplotlib.pyplot as plt

ratio = 14.7887

df = pd.read_csv("./myenv/coordinates.csv", header=None)

df2 = pd.read_csv("test_coords3.csv", header=None, index_col=False)
# print(df2)
# df2 = df2.transpose()
# z22 = df2.loc[2]
# print(df[0])
# df2 = df2 * ratio

# My coords
x2 = df2.loc[0]
y2 = df2.loc[1]
z2 = df2.loc[2]
# print(z2)
# print(max(z2))

# # Shift over and down
# third = max(x2) / 3      # get 1/3 of max T1 value
# twothirds = third * 2

# # Shift path to zero height (number from height of first graph)
# footshift = ratio * 11.45

# # Adjust footpath? IDK how
# x2 = x2-twothirds+15
# y2 = y2+footshift+75
# z2 = z2-footshift

# df3 = pd.DataFrame({'x': x2, 'y': y2, 'z': z2})

# print("Modified DataFrame:")
# print(df3)
# df3.to_csv("revised_with_ratios2.csv", index=False)

df4 = pd.read_csv("revised_with_ratios.csv", header=None)
df4 = df4.transpose()
# print(df4)
# # Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Extract the coordinate points
x1 = df.loc[0]
y1 = df.loc[1]
z1 = df.loc[2]

# My coords with ratios
x3 = df4.loc[0]
y3 = df4.loc[1]
z3 = df4.loc[2]

# print(x3)

# Plot the first set of points
ax.scatter(x1, y1, z1, c='r', marker='o', label='First Set')

# ax.scatter(x3, y3, z3, c='g', label='Third Set')

x = [0]
y = [0]
z = [0]

# Plot the single point
ax.scatter(x, y, z, c='g', marker='o')

# Plot the second set of points
ax.scatter(x2, y2, z2, c='b', marker='^', label='Second Set')

# # Set labels and title
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
ax.set_title('3D Scatter Plot')

# # Show the plot
plt.show()
