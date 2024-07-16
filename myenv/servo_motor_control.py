# Katie Sugg
# Summer 2024 WVU REU Robotics

import sys
import dynamixel_sdk as dynamixel
import pandas as pd
import numpy as np
from strain_collection import read_strain


# Change CSV name to correct file/file path
csv1 = "joint_angles2.csv"
csv = "thetas.csv"

# Make Pandas dataframe
df = pd.read_csv(csv, header=None)
df1 = pd.read_csv(csv1, header=None)

# TODO: joint_angles.csv has 4 rows for some reason. WIP


df1 = df1.drop([0], axis=0)

# Convert to Dynamixel units
GoalAngles = pd.DataFrame(np.round(np.rad2deg(df) / 0.088 + 2048).astype(int))
print(GoalAngles)
# GoalAngles1 = pd.DataFrame(np.round(np.rad2deg(df1) / 0.088 + 2048).astype(int))
# print(GoalAngles1)


# Number of steps
steps = 11

# Number of coordinates
numCommands = len(GoalAngles.columns)

# Strain collection settings with openCM
comportOpenCM = "/dev/tty.usbmodem14101"  # set to whatever openCM port is
baudOpenCM = float(1000000)               # set baudrate

# Change depending on number of input pins
desired_len = 10

# Create empty dataframe
strains = pd.DataFrame(columns=range(desired_len))


# Uses DYNAMIXEL SDK library
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

ESC_ASCII_VALUE = 0x1b      # Key for escaping loop

COMM_SUCCESS = 0            # Communication Success result value
COMM_TX_FAIL = -1001        # Communication Tx Failed


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


# Get input
def getch() -> str | int:
    return sys.stdin.read(1)


# Initialize PortHandler Structs
port_num = dynamixel.PortHandler(DEVICENAME)

# Initialize PacketHandler Structs
correct_protocol = dynamixel.PacketHandler(PROTOCOL_VERSION)


dxl_comm_result = COMM_TX_FAIL                 # Communication result
dxl_addparam_result = False                    # AddParam result
dxl_getdata_result = False                     # GetParam result

dxl_error = 0                                  # Dynamixel error


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


# Step the leg!
while 1:
    # lift the leg to the first pos
    setMXpositions(GoalAngles[0], groupwrite_num_pos)

    print("Press any key to continue! (or press ESC and then return to quit!)")
    if getch() == chr(ESC_ASCII_VALUE):
        break

    # Set velocities
    setMXvelocities([0, 0, 0], groupwrite_num_vel)

    # Loop through steps
    for j in range(1, steps):
        # Loop through number of footpath coordinates
        for i in range(1, numCommands-1):
            # Set position of leg
            setMXpositions(GoalAngles[i], groupwrite_num_pos)

            # Read groupsync
            groupread_num.txRxPacket()

            # Read strain for each step except 1st step
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

            # Make sure groupsync works
            for count in range(0, len(DXL_ID)):
                # Check if groupsyncread data of Dynamixel is available
                dxl_getdata_result = groupread_num.isAvailable(
                    DXL_ID[count], ADDR_PRESENT_POSITION,
                    LEN_PRESENT_POSITION)
                if dxl_getdata_result is not True:
                    print('groupSyncRead getdata failed ID', DXL_ID[count])


# Exit while loop
print("we're out")

# WIP save strains
print(strains)

# Close port
port_num.closePort()
