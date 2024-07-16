# Katie Sugg
# Summer 2024 WVU REU Robotics

# TODO: Speed code WIP
# Just a partial python translation of Isabella's speed incorporation
# into leg stepping

import time
import sys
import dynamixel_sdk as dynamixel
import pandas as pd
import math
import numpy as np
from strain_collection import read_strain


# Change CSV name to correct file/file path
# csv = "joint_angles.csv"
csv = "thetas.csv"

# Make Pandas dataframe
df = pd.read_csv(csv, header=None)

# TODO: joint_angles.csv has 4 rows for some reason. WIP
goalPos1 = np.array(df.iloc[0])
goalPos2 = np.array(df.iloc[1])
goalPos3 = np.array(df.iloc[2])
# goalPos1 = df.iloc[1]
# goalPos2 = df.iloc[2]
# goalPos3 = df.iloc[3]


# df = df.drop([0], axis=0)

# Convert to Dynamixel units
GoalAngles = pd.DataFrame(np.round(np.rad2deg(df) / 0.088 + 2048).astype(int))


# Number of steps
steps = 11

timeswing = 2    # Seconds
timestance = 2   # Seconds
totaltime = timeswing+timestance
numCommands = len(GoalAngles.columns)
dtswing = timeswing/numCommands
dtstance = timestance/numCommands
dt = totaltime/numCommands

# # TODO: make sure calulcations are corrct
Aswing = 1/(2*math.pi*dtswing)
Astance = 1/(2*math.pi*dtstance)

speed1 = np.zeros(numCommands)
speed2 = np.zeros(numCommands)
speed3 = np.zeros(numCommands)

# Set speed
# TODO: Why is it broken up into 3 for loops?
for i in range(1, 59):
    speed1[i] = round(Aswing * (abs(goalPos1[i] - goalPos1[i-1])))
    speed2[i] = round(Aswing * (abs(goalPos2[i] - goalPos2[i-1])))
    speed3[i] = round(Aswing * (abs(goalPos3[i] - goalPos3[i-1])))

# should this be 0 and 1?
speed1[1] = speed1[2]
speed2[1] = speed2[2]
speed3[1] = speed3[2]

for i in range(60, 179):
    speed1[i] = round(Astance * (abs(goalPos1[i] - goalPos1[i-1])))
    speed2[i] = round(Astance * (abs(goalPos2[i] - goalPos2[i-1])))
    speed3[i] = round(Astance * (abs(goalPos3[i] - goalPos3[i-1])))


for i in range(180, 240):
    speed1[i] = round(Aswing * (abs(goalPos1[i] - goalPos1[i-1])))
    speed2[i] = round(Aswing * (abs(goalPos2[i] - goalPos2[i-1])))
    speed3[i] = round(Aswing * (abs(goalPos3[i] - goalPos3[i-1])))


GoalPos = pd.DataFrame([goalPos1, goalPos2, goalPos3])
HalfPos = pd.DataFrame([np.zeros(len(goalPos1)), np.zeros(
    len(goalPos1)), np.zeros(len(goalPos1))])
# Is halPos supposed to be like goalpos?


# count = 1
# # idk what this is doing
# for i in range(len(df.columns)):
#     if i % 3:
#         HalfPos.append(df.iloc[i].values)
#         count += 1


GoalPos = HalfPos
speed1 = np.zeros(len(goalPos1))
speed2 = np.zeros(len(goalPos1))
speed3 = np.zeros(len(goalPos1))

dt = totaltime/numCommands
Astance = 1/(2*math.pi*dt/60)


# GoalAngles = GoalPos * 0.088   # deg
# GoalAngles = GoalPos.applymap(lambda x: x * 0.88)
# GoalAngles = [[elem * 0.88 for elem in row] for row in GoalPos]
# GoalRev = GoalAngles / 360    # rev
# GoalRev = [[elem / 360 for elem in row] for row in GoalPos]


# idk what this part is
speed1[1] = speed1[2]
speed2[1] = speed2[2]
speed3[1] = speed3[2]

# for i in range(2, numCommands):
#     speed1[i] = (GoalRev[0][i]-GoalRev[0][i-1])/(dt/60)     # rev/min
#     speed2[i] = (GoalRev[1][i]-GoalRev[1][i-1])/(dt/60)
#     speed3[i] = (GoalRev[2][i]-GoalRev[2][i-1])/(dt/60)

# Speed1 = pd.DataFrame([speed1, speed2, speed3])
# Speed2 = abs(round(Speed1/0.299))

# Speed2 = pd.DataFrame([[abs(round(elem / 0.299)) for elem in row] for row in Speed1])
# print(Speed2)

# print("works 123")


# # row
# for j in range(1, len(Speed2[0])):
#     # col
#     for i in range(1, len(Speed2)):
#         if Speed2[i][j] == 0:
#             Speed2[i][j] = 1

# Speed2[1, :] = 0   # may need to take abs of speed

# print(Speed2)


# setMXpositions
def setMXpositions(pos_vector, groupwrite_num_pos) -> None:
    pos_vector = np.array(pos_vector)

    for i in range(0, len(pos_vector)):
        # Add Dynamixel goal position value to the Syncwrite storage
        param_goal_position = [dynamixel.DXL_LOBYTE(
            dynamixel.DXL_LOWORD(int(pos_vector[i]))),
            dynamixel.DXL_HIBYTE(
            dynamixel.DXL_LOWORD(int(pos_vector[i]))),
            dynamixel.DXL_LOBYTE(
            dynamixel.DXL_HIWORD(int(pos_vector[i]))),
            dynamixel.DXL_HIBYTE(
            dynamixel.DXL_HIWORD(int(pos_vector[i])))]
        dxl_addparam_result = groupwrite_num_pos.addParam(
            DXL_ID[i], param_goal_position)

        if dxl_addparam_result is not True:
            print(f'ID {DXL_ID[i]} groupSyncWrite addParam failed')

    # Syncwrite goal position
    dxl_comm_result = groupwrite_num_pos.txPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % groupwrite_num_pos.getTxRxResult(dxl_comm_result))

    # Clear syncwrite parameter storage
    groupwrite_num_pos.clearParam()

# setMXveolcities


def setMXvelocities(vel_vector, groupwrite_num_vel) -> None:
    vel_vector = np.array(vel_vector)

    for i in range(0, len(vel_vector)):
        # Add Dynamixel goal position value to the Syncwrite storage
        param_goal_velocity = [dynamixel.DXL_LOBYTE(
            dynamixel.DXL_LOWORD(int(vel_vector[i]))),
            dynamixel.DXL_HIBYTE(
            dynamixel.DXL_LOWORD(int(vel_vector[i]))),
            dynamixel.DXL_LOBYTE(
            dynamixel.DXL_HIWORD(int(vel_vector[i]))),
            dynamixel.DXL_HIBYTE(
            dynamixel.DXL_HIWORD(int(vel_vector[i])))]
        dxl_addparam_result = groupwrite_num_vel.addParam(
            DXL_ID[i], param_goal_velocity)

        if dxl_addparam_result is not True:
            print('ID groupSyncWrite addparam failed', DXL_ID[i])

    dxl_comm_result = groupwrite_num_vel.txPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % groupwrite_num_vel.getTxRxResult(dxl_comm_result))

    # Clear syncwrite parameter storage
    groupwrite_num_vel.clearParam()


# Uses DYNAMIXEL SDK library
def getch() -> str | int:
    return sys.stdin.read(1)


# Control table address
ADDR_TORQUE_ENABLE = 64
ADDR_GOAL_POSITION = 116
ADDR_PRESENT_POSITION = 132
ADDR_PROFILE_VELOCITY = 112
LEN_PRESENT_POSITION = 4
LEN_GOAL_POSITION = 4
LEN_GOAL_VELOCITY = 4
LEN_PROFILE_VELOCITY = 4
BAUDRATE = 1000000


# Protocol version
PROTOCOL_VERSION = 2

# Default setting
DXL1_ID = 1            # Dynamixel#1 ID: 1
DXL2_ID = 2            # Dynamixel#2 ID: 2
DXL3_ID = 3            # Dynamixel#2 ID: 3
DXL_ID = [DXL1_ID, DXL2_ID, DXL3_ID]
BAUDRATE = 1000000
# DEVICENAME = 'COM7'       # Check which port is being used on your controller
DEVICENAME = "/dev/tty.usbserial-FT78LNE8"

TORQUE_ENABLE = 1            # Value for enabling the torque
TORQUE_DISABLE = 0            # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 20           # Dynamixel moving status threshold

# Key for escaping loop
ESC_ASCII_VALUE = 0x1b


COMM_SUCCESS = 0            # Communication Success result value
COMM_TX_FAIL = -1001        # Communication Tx Failed

# Initialize PortHandler Structs
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
port_num = dynamixel.PortHandler(DEVICENAME)

# Initialize PacketHandler Structs
correct_protocol = dynamixel.PacketHandler(PROTOCOL_VERSION)

# Initalizing with zeros and not NaN
servo1 = np.zeros((steps, numCommands))
servo2 = np.zeros((steps, numCommands))
servo3 = np.zeros((steps, numCommands))

positions = np.zeros((numCommands, 3))

dxl_comm_result = COMM_TX_FAIL                 # Communication result
dxl_addparam_result = False                    # AddParam result
dxl_getdata_result = False                     # GetParam result

dxl_error = 0                                  # Dynamixel error
# positions = np.zeros(len(DXL_ID))          # Present Positions

stepTime = np.zeros((steps, numCommands))
oneStepTime = np.zeros(steps)
strains = np.zeros((6, numCommands))

# Initialize Groupsync Structs
groupwrite_num_pos = dynamixel.GroupSyncWrite(port=port_num,
                                              ph=correct_protocol,
                                              start_address=ADDR_GOAL_POSITION,
                                              data_length=LEN_GOAL_POSITION)
groupwrite_num_vel = dynamixel.GroupSyncWrite(port_num,
                                              correct_protocol,
                                              ADDR_PROFILE_VELOCITY,
                                              LEN_PROFILE_VELOCITY)
groupread_num = dynamixel.GroupSyncRead(port_num,
                                        correct_protocol,
                                        ADDR_PRESENT_POSITION,
                                        LEN_PRESENT_POSITION)

# Open port
if port_num.openPort():
    print("Succeeded to open the port!")
else:
    print("Failed to open the port!")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate
if port_num.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate!")
else:
    print("Failed to change the baudrate!")
    print("Press any key to terminate...")
    getch()
    quit()


comportOpenCM = "/dev/tty.usbmodem14101"  # set to whatever openCM port is
baudOpenCM = float(1000000)
# openCM = serialport(comportOpenCM,baudOpenCM)
# openCM.flush()
# IDstrain = [1, 2, 3, 4, 5, 6]
# # what should strains look like?  10 x 118 double?
# strains = pd.DataFrame(0, index=np.arange(
#     steps-1), columns=np.arange(len(goalPos1)))

# strain1 = pd.DataFrame(0, index=np.arange(
#     steps-1), columns=np.arange(len(goalPos1)))
# strain2 = pd.DataFrame(0, index=np.arange(
#     steps-1), columns=np.arange(len(goalPos1)))
# strain3 = pd.DataFrame(0, index=np.arange(
#     steps-1), columns=np.arange(len(goalPos1)))
# strain4 = pd.DataFrame(0, index=np.arange(
#     steps-1), columns=np.arange(len(goalPos1)))
# strain5 = pd.DataFrame(0, index=np.arange(
#     steps-1), columns=np.arange(len(goalPos1)))
# strain6 = pd.DataFrame(0, index=np.arange(
#     steps-1), columns=np.arange(len(goalPos1)))


for i in range(0, len(DXL_ID)):
    # Enable Dynamixel Torque
    dxl_comm_result, dxl_error = correct_protocol.write1ByteTxRx(port_num,
                                                                 DXL_ID[i],
                                                                 ADDR_TORQUE_ENABLE,
                                                                 TORQUE_ENABLE)

    if dxl_comm_result != COMM_SUCCESS:
        print(
            f"Dynamixel {DXL_ID[i]}: {correct_protocol.getTxRxResult(dxl_comm_result)}")
    elif dxl_error != 0:
        print(
            f"Dynamixel {DXL_ID[i]}: {correct_protocol.getRxPacketError(dxl_error)}")
    else:
        print(f"Dynamixel {DXL_ID[i]} has been successfully connected")

    #  Add parameter storage for Dynamixel#1 present position value
    dxl_addparam_result = groupread_num.addParam(DXL_ID[i])
    if dxl_addparam_result is not True:
        print('ID groupSyncRead addparam failed', DXL_ID[i])
    else:
        print('groupSyncRead addparam worked!')


# Change depending on number of input pins
desired_len = 10

# Create empty dataframe
strains = pd.DataFrame(columns=range(desired_len))


# Step the leg!
while 1:
    # lift the leg to the first pos
    setMXpositions(GoalAngles[0], groupwrite_num_pos)
    # writeTime = time.time() - writeTime  # toc(writeTime)
    # readTime = time.time()  # tic
    # readTime = time.time() - readTime  # toc(readTime)

    print("Press any key to continue! (or press ESC and then return to quit!)")
    if getch() == chr(ESC_ASCII_VALUE):
        break

    setMXvelocities([0, 0, 0], groupwrite_num_vel)
    for j in range(1, steps):
        # oneStep = time.time()  # tic
        # timer = time.time()  # tic
        for i in range(1, numCommands-1):
            # steptime = time.time()  # tic
            setMXpositions(GoalAngles[i], groupwrite_num_pos)
            groupread_num.txRxPacket()

            if j == 1:
                pass
            else:
                # Read and store strain output as an array
                output = read_strain(comportOpenCM, baudOpenCM)

                # Deal with cases where output != desired_len
                if len(output) > desired_len:
                    # Truncates extra numbers
                    output = output[:desired_len]
                elif (len(output) < desired_len):
                    # Pads with NaN to reach desired_len
                    output = output + [np.nan] * (desired_len - len(output))

                # Adds output as a row to dataframe
                strains.loc[len(strains)] = output

            for count in range(0, len(DXL_ID)):
                # Check if groupsyncread data of Dynamixel is available
                dxl_getdata_result = groupread_num.isAvailable(
                    DXL_ID[count], ADDR_PRESENT_POSITION,
                    LEN_PRESENT_POSITION)
                if dxl_getdata_result is not True:
                    print('groupSyncRead getdata failed ID', DXL_ID[count])

                # # Get Dynamixel present position value
                # positions[i, count] = groupread_num.getData(
                #     DXL_ID[count], ADDR_PRESENT_POSITION,
                #     LEN_PRESENT_POSITION)

            # servo1[j, i] = positions[i, 0]
            # servo2[j, i] = positions[i, 1]
            # servo3[j, i] = positions[i, 2]

            # # toc(steptime)
            # while (time.time() - steptime) < dt:
            #     pass

            # # toc(timer)
            # stepTime[j, i] = time.time() - timer

        # toc(oneStep)
        # oneStepTime[j] = time.time() - oneStep
        # print(strain1[j, :])
        # print(strains[0, :])
        # strain1[j, :] = strains[0, :]
        # strain2[j, :] = strains[1, :]
        # strain3[j, :] = strains[2, :]
        # strain4[j, :] = strains[3, :]
        # strain5[j, :] = strains[4, :]
        # strain6[j, :] = strains[5, :]


print("we're out")
print(strains)
# Close port
port_num.closePort()


# Code works
