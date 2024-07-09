# Note the dynamixels on the robot leg are MX - 28

# Uses DYNAMIXEL SDK library
import dynamixel_sdk as dynamixel
import sys


def getch():
    return sys.stdin.read(1)


# Control table address
# Control table address is different in Dynamixel model
ADDR_PRO_TORQUE_ENABLE = 24
ADDR_PRO_GOAL_POSITION = 30
ADDR_PRO_PRESENT_POSITION = 36

# Protocol version
# See which protocol version is used in the Dynamixel
# PROTOCOL_VERSION = 2
PROTOCOL_VERSION = 1.0

# Default setting
DXL_ID = 1                             # Dynamixel ID: 1
BAUDRATE = 57600
# Check which port is being used on your controller
DEVICENAME = "/dev/tty.usbserial-FT62AOBZ"

# ex) Windows: "COM1"   Linux: "/dev/ttyUSB0"

TORQUE_ENABLE = 1                             # Value for enabling the torque
TORQUE_DISABLE = 0                             # Value for disabling the torque
# Dynamixel will rotate between this value
DXL_MINIMUM_POSITION_VALUE = -150000
# and this value (note that the Dynamixel would not move when the position
# value is out of movable range. Check e-manual about the range of the
# Dynamixel you use.)
DXL_MAXIMUM_POSITION_VALUE = 150000
# Dynamixel moving status threshold
DXL_MOVING_STATUS_THRESHOLD = 20

ESC_ASCII_VALUE = 0x1b

COMM_SUCCESS = 0                       # Communication Success result value
COMM_TX_FAIL = -1001                         # Communication Tx Failed

# Initialize PortHandler Structs
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
port_num = dynamixel.PortHandler(DEVICENAME)

# Initialize PacketHandler Structs
correct_protocol = dynamixel.PacketHandler(PROTOCOL_VERSION)

index = 0
# Communication result
dxl_comm_result = COMM_TX_FAIL
dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE,
                     DXL_MAXIMUM_POSITION_VALUE]         # Goal position

dxl_error = 0                                               # Dynamixel error
dxl_present_position = 0                                    # Present position

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


# Enable Dynamixel Torque
correct_protocol.write1ByteTxRx(port_num,
                                DXL_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)

while 1:
    print("Press any key to continue! (or press ESC to quit!)")
    if getch() == chr(ESC_ASCII_VALUE):
        break

    # Write goal position
    correct_protocol.write4ByteTxRx(port_num, DXL_ID,
                                    ADDR_PRO_GOAL_POSITION,
                                    dxl_goal_position[index])

    dxl_comm_result, dxl_error = correct_protocol.write4ByteTxRx(
        port_num, DXL_ID, ADDR_PRO_GOAL_POSITION, dxl_goal_position[index])
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % correct_protocol.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % correct_protocol.getRxPacketError(dxl_error))

    while 1:
        # Read present position
        dxl_present_position, dxl_comm_result, dxl_error = correct_protocol.read4ByteTxRx(
            port_num, DXL_ID, ADDR_PRO_PRESENT_POSITION)

        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % correct_protocol.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % correct_protocol.getRxPacketError(dxl_error))

        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" %
              (DXL_ID, dxl_goal_position[index], dxl_present_position))

        if not (abs(dxl_goal_position[index] - dxl_present_position) >
                DXL_MOVING_STATUS_THRESHOLD):
            break

    # Change goal positionn
    if index == 0:
        index = 1
    else:
        index = 0

# something is going on
print("here")

# Disable Dynamixel Torque
dxl_comm_result, dxl_error = correct_protocol.write1ByteTxRx(
    port_num, PROTOCOL_VERSION, DXL_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)

if dxl_comm_result != COMM_SUCCESS:
    print("%s" % correct_protocol.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % correct_protocol.getRxPacketError(dxl_error))


# Close port
port_num.closePort(port_num)

# End of my dynamixel code
