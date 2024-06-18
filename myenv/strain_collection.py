import serial
import numpy as np


def read_strain(port_path: str, baudrate: int):
    ser = serial.Serial(port_path, baudrate)  # open serial port
    # ser.timeout = 1 ?
    print(ser.name)         # check which port was really used

    ser.open()
    if not ser.is_open():
        raise Exception("Serial port is not open.")

    ser.reset_input_buffer()
    ser.write(bytes([1]))
    IDs = [1, 2, 3, 4, 5, 6]

    while ser.in_waiting == 0:
        # Wait for a byte to arrive
        pass

    i = 0
    data = []
    strain = np.full(len(IDs), np.nan)

    while ser.in_waiting:
        # Reads 1 byte and converts into an integer
        data.append(int.from_bytes(ser.read(1)))

        if i >= 3:
            # Calculate the checksum
            checksum = data[i-1] + data[i-2] + data[i-3]
            if checksum == data[i]:
                # Checksum matches, save the strain info
                low_byte = data[i-2]
                high_byte = data[i-1]
                try:
                    strain[data[i-3] - 1] = high_byte * 256 + low_byte
                except IndexError:
                    pass

        i += 1

    ser.close()             # close port

    return strain
