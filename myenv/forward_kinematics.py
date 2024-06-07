# import numpy as np
# import modern_robotics as mr
import pandas as pd
# import pandas module

# making dataframe
df = pd.read_csv("coordinates.csv", header=None)

# output the dataframe
print(df)
print(df[0].tolist())
