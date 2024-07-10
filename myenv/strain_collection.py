import serial
import pandas as pd
import numpy as np


def read_strain(port_path: str, baudrate: int):
    # Opens serial port
    ser = serial.Serial(port_path, baudrate)

    # Empty buffer and sends byte to start recieving data
    # ser.reset_input_buffer()
    ser.flushInput()
    ser.write(bytes([1]))

    # Wait for byte to arrive
    while ser.in_waiting == 0:
        pass

    # Initalize enpty strain list
    strain = []

    # Data has arrived
    while ser.in_waiting:
        # Initalize temporarly data list
        data = []
        # Reads 4 bytes and appends to data list
        # 4 because of how packets are structured and sent
        data.append(int.from_bytes(ser.read(1), 'big'))
        data.append(int.from_bytes(ser.read(1), 'big'))
        data.append(int.from_bytes(ser.read(1), 'big'))
        data.append(int.from_bytes(ser.read(1), 'big'))

        # Checksum matches, save the strain info
        checksum = data[0] + data[1] + data[2]
        if checksum == data[3]:
            low_byte = data[1]
            high_byte = data[2]
            try:
                # Adds strain value to strain list
                strain.append(high_byte * 256 + low_byte)
            except IndexError:
                pass

    ser.close()
    # Returns strain list
    return strain


def main():
    # Change depending on number of input pins
    desired_len = 10

    # Create empty dataframe
    df = pd.DataFrame(columns=range(desired_len))

    # Change for desired number of data points
    data_points = 1000
    i = 0
    while i < data_points:
        # Store strain output as an array
        output = read_strain("/dev/tty.usbmodem14101", 1000000)

        # Deal with cases where output != desired_len
        if len(output) > desired_len:
            # Truncates extra numbers
            output = output[:desired_len]
        elif (len(output) < desired_len):
            # Pads with NaN to reach desired_len
            output = output + [np.nan] * (desired_len - len(output))

        # Adds output as a row to dataframe
        df.loc[len(df)] = output
        i += 1

    # Ouputs dataframe to csv
    df.to_csv("strain.csv", index=False)


# Automatically runs main when you run the file
if __name__ == "__main__":
    main()
