import time
import sys
import dynamixel_sdk as dynamixel
import pandas as pd
# import math
import numpy as np

# Change CSV name to correct file/file path
# csv = "joint_angles.csv"
csv = "thetas.csv"

# Make Pandas dataframe
df = pd.read_csv(csv, header=None)

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
# numCommands = len(goalPos1)
numCommands = 239
dtswing = timeswing/numCommands
dtstance = timestance/numCommands
dt = totaltime/numCommands

# GoalPos = [goalPos1, goalPos2, goalPos3]


def setMXpositions(pos_vector, groupwrite_num_pos):
    DXL_ID = [1, 2, 3]
    pos_vector = np.array(pos_vector)

    for i in range(0, len(pos_vector)):
        # Add Dynamixel goal position value to the Syncwrite storage
        param_goal_position = [dynamixel.DXL_LOBYTE(dynamixel.DXL_LOWORD(int(pos_vector[i]))),
                               dynamixel.DXL_HIBYTE(
                                   dynamixel.DXL_LOWORD(int(pos_vector[i]))),
                               dynamixel.DXL_LOBYTE(
                                   dynamixel.DXL_HIWORD(int(pos_vector[i]))),
                               dynamixel.DXL_HIBYTE(dynamixel.DXL_HIWORD(int(pos_vector[i])))]
        dxl_addparam_result = groupwrite_num_pos.addParam(
            DXL_ID[i], param_goal_position)

        if dxl_addparam_result is not True:
            print(f'ID {DXL_ID[i]} groupSyncWrite addParam failed')

    # Syncwrite goal position
    dxl_comm_result = groupwrite_num_pos.txPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % groupwrite_num_pos.getTxRxResult(dxl_comm_result))

    # # WIP error checking
    # dxl_comm_result = correct_protocol.write4ByteTxRx(port_num, DXL2_ID,
    #                                                   ADDR_PRO_GOAL_POSITION, dxl2_goal_position[index])
    # if dxl_comm_result is not COMM_SUCCESS:
    #     # getTxRxResult is also not a function I can find
    #     print('%s\n', correct_protocol.getTxRxResult(
    #         dxl_comm_result))

    # Clear syncwrite parameter storage
    groupwrite_num_pos.clearParam()


def setMXvelocities(vel_vector, groupwrite_num_vel):
    DXL_ID = [1, 2, 3]
    LEN_PROFILE_VELOCITY = 4

    for i in range(0, len(vel_vector)):
        # Add Dynamixel goal position value to the Syncwrite storage
        dxl_addparam_result = dynamixel.GroupSyncWrite.addParam(
            groupwrite_num_vel, DXL_ID[i],
            LEN_PROFILE_VELOCITY)
        if dxl_addparam_result is not True:
            print('ID groupSyncWrite addparam failed', DXL_ID[i])

    groupwrite_num_vel.txPacket()

    # WIP error checking
    # dxl_comm_result = dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION)
    # if dxl_comm_result is not COMM_SUCCESS:
    #     print('%s\n', dynamixel.getTxRxResult(
    #         PROTOCOL_VERSION, dxl_comm_result))

    # Clear syncwrite parameter storage
    groupwrite_num_vel.clearParam()


# Uses DYNAMIXEL SDK library
def getch():
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

# ESC_CHARACTER                   = 'e';          # Key for escaping loop
ESC_ASCII_VALUE = 0x1b

COMM_SUCCESS = 0            # Communication Success result value
COMM_TX_FAIL = -1001        # Communication Tx Failed

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

# stepTime = np.zeros(steps, numCommands)
# oneStepTime = np.zeros(1, steps)
strains = np.zeros((6, numCommands))

# Initialize Groupsync Structs
groupwrite_num_pos = dynamixel.GroupSyncWrite(port=port_num,
                                              ph=correct_protocol,
                                              start_address=ADDR_GOAL_POSITION,
                                              data_length=LEN_GOAL_POSITION)

groupwrite_num_vel = dynamixel.GroupSyncWrite(port=port_num,
                                              ph=correct_protocol,
                                              start_address=ADDR_PROFILE_VELOCITY,
                                              data_length=LEN_PROFILE_VELOCITY)
groupread_num = dynamixel.GroupSyncRead(port=port_num,
                                        ph=correct_protocol,
                                        start_address=ADDR_PRESENT_POSITION,
                                        data_length=LEN_PRESENT_POSITION)

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


# strain1 = np.zeros((steps-1, len(goalPos1)))
# strain2 = np.zeros((steps-1, len(goalPos1)))
# strain3 = np.zeros((steps-1, len(goalPos1)))
# strain4 = np.zeros((steps-1, len(goalPos1)))
# strain5 = np.zeros((steps-1, len(goalPos1)))
# strain6 = np.zeros((steps-1, len(goalPos1)))

while 1:
    # lift the leg to the first pos
    writeTime = time.time()  # tic
    setMXpositions(GoalAngles[0], groupwrite_num_pos)
    writeTime = time.time() - writeTime  # toc(writeTime)
    readTime = time.time()  # tic
    readTime = time.time() - readTime  # toc(readTime)

    print("Press any key to continue! (or press ESC to quit!)")
    if getch() == chr(ESC_ASCII_VALUE):
        break

    # setMXvelocities([0, 0, 0], groupwrite_num_vel)
    for j in range(1, steps-1):
        oneStep = time.time()  # tic
        timer = time.time()  # tic
        for i in range(1, numCommands-1):
            steptime = time.time()  # tic
            setMXpositions(GoalAngles[i], groupwrite_num_pos)

            groupread_num.txRxPacket()

            for count in range(0, len(DXL_ID)):
                # Check if groupsyncread data of Dynamixel is available
                dxl_getdata_result = groupread_num.isAvailable(
                    DXL_ID[count], ADDR_PRESENT_POSITION,
                    LEN_PRESENT_POSITION)
                if dxl_getdata_result is not True:
                    print('groupSyncRead getdata failed ID', DXL_ID[count])

                # Get Dynamixel present position value
                positions[i, count] = groupread_num.getData(
                    DXL_ID[count], ADDR_PRESENT_POSITION,
                    LEN_PRESENT_POSITION)

            servo1[j, i] = positions[i, 0]
            servo2[j, i] = positions[i, 1]
            servo3[j, i] = positions[i, 2]

# Close port
port_num.closePort()
