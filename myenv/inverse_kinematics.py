import pandas as pd

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

# print(array_of_coordinates)
print(df[0].tolist())
