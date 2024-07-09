import time
import sys
import dynamixel_sdk as dynamixel
import pandas as pd
import math
import numpy as np
# from strain_collection import readstrain


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

# # TODO: make sure calulcations are corrct
Aswing = 1/(2*math.pi*dtswing)
Astance = 1/(2*math.pi*dtstance)

speed1 = np.zeros((1, len(goalPos1)))
speed2 = np.zeros((1, len(goalPos1)))
speed3 = np.zeros((1, len(goalPos1)))

# # Set speed
# # TODO: Why is it broken up into 3 for loops?
# for i in range(2, 60):
#     speed1[i] = round(Aswing * (abs(goalPos1[i] - goalPos1[i-1])))
#     speed2[i] = round(Aswing * (abs(goalPos2[i] - goalPos2[i-1])))
#     speed3[i] = round(Aswing * (abs(goalPos3[i] - goalPos3[i-1])))

# # should this be 0 and 1?
# speed1[1] = speed1[2]
# speed2[1] = speed2[2]
# speed3[1] = speed3[2]

# for i in range(61, 180):
#     speed1[i] = round(Astance * (abs(goalPos1[i] - goalPos1[i-1])))
#     speed2[i] = round(Astance * (abs(goalPos2[i] - goalPos2[i-1])))
#     speed3[i] = round(Astance * (abs(goalPos3[i] - goalPos3[i-1])))


# for i in range(181, 240):
#     speed1[i] = round(Aswing * (abs(goalPos1[i] - goalPos1[i-1])))
#     speed2[i] = round(Aswing * (abs(goalPos2[i] - goalPos2[i-1])))
#     speed3[i] = round(Aswing * (abs(goalPos3[i] - goalPos3[i-1])))


GoalPos = [goalPos1, goalPos2, goalPos3]
HalfPos = [np.zeros((1, len(goalPos1))), np.zeros((
    1, len(goalPos1))), np.zeros((1, len(goalPos1)))]
# # Is halPos supposed to be like goalpos?


# count = 1

# for i in range(1, len(GoalPos[:,  1])):
#     if i % 3:
#         HalfPos[count, :] = GoalPos[i, :]
#         count += 1


# GoalPos = HalfPos
# speed1 = np.zeros(1, len(goalPos1))
# speed2 = np.zeros(1, len(goalPos1))
# speed3 = np.zeros(1, len(goalPos1))

# numCommands = len(GoalPos)
# dt = totaltime/numCommands
# Astance = 1/(2*math.pi*dt/60)

# GoalAngles = GoalPos * 0.088   # deg
# GoalRev = GoalAngles / 360    # rev

# # should this be 0?
# speed1[1] = 0
# speed2[1] = 0
# speed3[1] = 0
# for i in range(2, numCommands):
#     speed1[i] = (GoalRev[i, 1]-GoalRev[i-1, 1])/(dt/60)     # rev/min
#     speed2[i] = (GoalRev[i, 2]-GoalRev[i-1, 2])/(dt/60)
#     speed3[i] = (GoalRev[i, 3]-GoalRev[i-1, 3])/(dt/60)

# Speed1 = [speed1, speed2, speed3]
# Speed2 = abs(round(Speed1/0.299))


# for j in range(1, len(Speed2[1, :])):
#     for i in range(1, len(Speed2[:, 1])):
#         if Speed2[i, j] == 0:
#             Speed2[i, j] = 1

# Speed2[1, :] = 0   # may need to take abs of speed


# setMXpositions
def setMXpositions(pos_vector, groupwrite_num_pos):
    DXL_ID = [1, 2, 3]
    # groupwrite_num_pos = 0
    LEN_GOAL_POSITION = 4
    # port_num = 0
    # PROTOCOL_VERSION = 2
    # COMM_SUCCESS = 0

    # for i in range(0, len(pos_vector)):
    for i in range(0, 3):
        # Add Dynamixel goal position value to the Syncwrite storage
        dxl_addparam_result = dynamixel.GroupSyncWrite.addParam(
            groupwrite_num_pos, DXL_ID[i], LEN_GOAL_POSITION)
        # dxl_addparam_result = groupwrite_num_pos.addParam(DXL_ID[i],
        #                                                   pos_vector)
        if dxl_addparam_result is not True:
            print('[ID:%03d] groupSyncWrite addparam failed', DXL_ID[i])

    # dynamixel.GroupSyncWrite.txPacket(groupwrite_num_pos)
    groupwrite_num_pos.txPacket()

    # idk if this is a function
    # dxl_comm_result = dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION)
    # if dxl_comm_result is not COMM_SUCCESS:
    #     # getTxRxResult is also not a function I can find
    #     print('%s\n', dynamixel.getTxRxResult(PROTOCOL_VERSION,
    #                                           dxl_comm_result))
    # Clear syncwrite parameter storage
    dynamixel.GroupSyncWrite.clearParam(groupwrite_num_pos)


# setMXveolcities
def setMXvelocities(vel_vector):
    DXL_ID = [1, 2, 3]
    # groupwrite_num_vel = 1
    LEN_PROFILE_VELOCITY = 4
    # port_num = 0
    # PROTOCOL_VERSION = 2
    # COMM_SUCCESS = 0

    for i in range(0, len(vel_vector)):
        # Add Dynamixel goal position value to the Syncwrite storage
        dxl_addparam_result = dynamixel.GroupSyncWrite.addParam(
            groupwrite_num_vel, DXL_ID[i],
            LEN_PROFILE_VELOCITY)
        if dxl_addparam_result is not True:
            print('[ID:%03d] groupSyncWrite addparam failed', DXL_ID[i])

    dynamixel.GroupSyncWrite.txPacket(groupwrite_num_vel)
    # # IDK if this function exisits
    # dxl_comm_result = dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION)
    # if dxl_comm_result is not COMM_SUCCESS:
    #     print('%s\n', dynamixel.getTxRxResult(
    #         PROTOCOL_VERSION, dxl_comm_result))

    # Clear syncwrite parameter storage
    dynamixel.GroupSyncWrite.clearParam(groupwrite_num_vel)


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
# stepTime = np.zeros(steps, numCommands)
# oneStepTime = np.zeros(1, steps)
strains = np.zeros(6, numCommands)

dxl_comm_result = COMM_TX_FAIL                 # Communication result
dxl_addparam_result = False                    # AddParam result
dxl_getdata_result = False                     # GetParam result

dxl_error = 0                                  # Dynamixel error
# positions = np.zeros(len(DXL_ID))          # Present Positions

# Initialize Groupsync Structs
groupwrite_num_pos = dynamixel.GroupSyncWrite(port=port_num,
                                              ph=correct_protocol,
                                              start_address=ADDR_GOAL_POSITION,
                                              data_length=LEN_GOAL_POSITION)
print(type(groupwrite_num_pos))
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


comportOpenCM = "COM6"  # set to whatever openCM port is
baudOpenCM = float(1000000)
# openCM = serialport(comportOpenCM,baudOpenCM)
# openCM.flush()
IDstrain = [1, 2, 3, 4, 5, 6]
# what should strains look like?  10 x 118 double?
strains = np.zeros((6, 6))

strain1 = np.zeros((steps-1, len(goalPos1)))
strain2 = np.zeros((steps-1, len(goalPos1)))
strain3 = np.zeros((steps-1, len(goalPos1)))
strain4 = np.zeros((steps-1, len(goalPos1)))
strain5 = np.zeros((steps-1, len(goalPos1)))
strain6 = np.zeros((steps-1, len(goalPos1)))


for i in range(0, len(DXL_ID)):
    # Enable Dynamixel Torque
    correct_protocol.write1ByteTxRx(port_num,
                                    DXL_ID[i], ADDR_TORQUE_ENABLE,
                                    TORQUE_ENABLE)

    #  Add parameter storage for Dynamixel#1 present position value
    dxl_addparam_result = dynamixel.GroupSyncRead.addParam(
        groupread_num, DXL_ID[i])
    if dxl_addparam_result is not True:
        print('[ID:%03d] groupSyncRead addparam failed', DXL_ID[i])
    else:
        print('groupSyncRead addparam worked!')


# Step the leg!
while 1:
    # lift the leg to the first pos
    writeTime = time.time()  # tic
    # setMXpositions(GoalPos[1, :])
    setMXpositions(np.array(GoalPos[1]), groupwrite_num_pos)
    writeTime = time.time() - writeTime  # toc(writeTime)
    readTime = time.time()  # tic
    # Positions=readMXpositions();
    readTime = time.time() - readTime  # toc(readTime)

    print("Press any key to continue! (or press ESC to quit!)")
    if getch() == chr(ESC_ASCII_VALUE):
        break

    # setMXvelocities([0, 0, 0])
    for j in range(0, steps):
        oneStep = time.time()  # tic
        timer = time.time()  # tic
        for i in range(0, numCommands):
            steptime = time.time()  # tic

            # setMXpositions(GoalPos[i, :])

            # positions(i,:)=readMXpositions();

            # IDK if there's a python equalvalent
            dynamixel.GroupSyncRead.txRxPacket(groupread_num)
            # dynamixel.GroupSyncRead.txRxPacket(port_num)
            # groupread_num.txRxPacket(port_num)

            # readstrain(port_path, baudrate)
            # idk how to get strain read by specific ID
            # strains[:, i] = readstrain(IDstrain, baudOpenCM)
            for count in range(0, len(DXL_ID)):
                # Check if groupsyncread data of Dynamixel is available
                dxl_getdata_result = dynamixel.GroupSyncRead.isAvailable(
                    groupread_num, DXL_ID[count], ADDR_PRESENT_POSITION,
                    LEN_PRESENT_POSITION)
                if dxl_getdata_result is not True:
                    print('groupSyncRead getdata failed ID', DXL_ID[count])

                # Get Dynamixel present position value
                positions[i, count] = dynamixel.GroupSyncRead.getData(
                    groupread_num, DXL_ID[count], ADDR_PRESENT_POSITION,
                    LEN_PRESENT_POSITION)

            servo1[j, i] = positions[i, 0]
            servo2[j, i] = positions[i, 1]
            servo3[j, i] = positions[i, 2]

            # toc(steptime)
            # while (time.time() - steptime) < dt:
            #     pass

            # toc(timer)
            # stepTime[j, i] = time.time() - timer

        # toc(oneStep)
        # oneStepTime[j] = time.time() - oneStep
        # strain1[j, :] = strains[1, :]
        # strain2[j, :] = strains[2, :]
        # strain3[j, :] = strains[3, :]
        # strain4[j, :] = strains[4, :]
        # strain5[j, :] = strains[5, :]
        # strain6[j, :] = strains[6, :]


# Close port
port_num.closePort(port_num)
