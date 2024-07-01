import pandas as pd
# from inverse_kinematics import inverse_k
import math
import numpy as np


# Change CSV name to correct file/file path
csv = "joint_angles.csv"

# Make Pandas dataframe
df = pd.read_csv(csv, header=None)

goalPos1 = df.iloc[1]
goalPos2 = df.iloc[2]
goalPos3 = df.iloc[3]
# print(goalPos1)

# Number of steps
steps = 11

timeswing = 2    # Seconds
timestance = 2   # Seconds
totaltime = timeswing+timestance
numCommands = len(goalPos1)
dtswing = timeswing/numCommands
dtstance = timestance/numCommands
dt = totaltime/numCommands

# TODO: make sure calulcations are corrct
Aswing = 1/(2*math.pi*dtswing)
Astance = 1/(2*math.pi*dtstance)

speed1 = np.zeros(1, len(goalPos1))
speed2 = np.zeros(1, len(goalPos1))
speed3 = np.zeros(1, len(goalPos1))

# Set speed
# TODO: Why is it broken up into 3 for loops?
for i in range(2, 60):
    speed1[i] = round(Aswing * (abs(goalPos1[i] - goalPos1[i-1])))
    speed2[i] = round(Aswing * (abs(goalPos2[i] - goalPos2[i-1])))
    speed3[i] = round(Aswing * (abs(goalPos3[i] - goalPos3[i-1])))

# should this be 0 and 1?
speed1[1] = speed1[2]
speed2[1] = speed2[2]
speed3[1] = speed3[2]

for i in range(61, 180):
    speed1[i] = round(Astance * (abs(goalPos1[i] - goalPos1[i-1])))
    speed2[i] = round(Astance * (abs(goalPos2[i] - goalPos2[i-1])))
    speed3[i] = round(Astance * (abs(goalPos3[i] - goalPos3[i-1])))


for i in range(181, 240):
    speed1[i] = round(Aswing * (abs(goalPos1[i] - goalPos1[i-1])))
    speed2[i] = round(Aswing * (abs(goalPos2[i] - goalPos2[i-1])))
    speed3[i] = round(Aswing * (abs(goalPos3[i] - goalPos3[i-1])))


GoalPos = [goalPos1, goalPos2, goalPos3]
HalfPos = [np.zeros(1, len(goalPos1)), np.zeros(
    1, len(goalPos1)), np.zeros(1, len(goalPos1))]
# Is halPos supposed to be like goalpos?

count = 1

for i in range(1, len(GoalPos[:,  1])):
    if i % 3:
        HalfPos[count, :] = GoalPos[i, :]
        count += 1


GoalPos = HalfPos
# clear HalfPos  # empty HalfPos?
# clear speed1 speed2 speed3
# I assume you're resetting speeds
speed1 = np.zeros(1, len(goalPos1))
speed2 = np.zeros(1, len(goalPos1))
speed3 = np.zeros(1, len(goalPos1))

numCommands = len(GoalPos)
dt = totaltime/numCommands
Astance = 1/(2*math.pi*dt/60)

GoalAngles = GoalPos * 0.088   # deg
GoalRev = GoalAngles / 360    # rev

# should this be 0?
speed1[1] = 0
speed2[1] = 0
speed3[1] = 0
for i in range(2, numCommands):
    speed1[i] = (GoalRev[i, 1]-GoalRev[i-1, 1])/(dt/60)     # rev/min
    speed2[i] = (GoalRev[i, 2]-GoalRev[i-1, 2])/(dt/60)
    speed3[i] = (GoalRev[i, 3]-GoalRev[i-1, 3])/(dt/60)

Speed1 = [speed1, speed2, speed3]
Speed2 = abs(round(Speed1/0.299))


for j in range(1, len(Speed2[1, :])):
    for i in range(1, len(Speed2[:, 1])):
        if Speed2[i, j] == 0:
            Speed2[i, j] = 1

Speed2[1, :] = 0   # may need to take abs of speed
