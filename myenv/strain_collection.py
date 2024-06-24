import serial
import pandas as pd


def read_strain(port_path: str, baudrate: int):
    ser = serial.Serial(port_path, baudrate)  # open serial port
    # ser.timeout = 1 ?
    # print(ser.name)         # check which port was really used

    # ser.open()
    # if not ser.is_open():
    #     raise Exception("Serial port is not open.")

    ser.reset_input_buffer()
    ser.write(bytes([1]))

    while ser.in_waiting == 0:
        # Wait for a byte to arrive
        pass

    strain = []

    while ser.in_waiting:
        # Reads 1 byte and converts into an integer
        data = []
        data.append(int.from_bytes(ser.read(1), 'big'))
        data.append(int.from_bytes(ser.read(1), 'big'))
        data.append(int.from_bytes(ser.read(1), 'big'))
        data.append(int.from_bytes(ser.read(1), 'big'))

        checksum = data[0] + data[1] + data[2]
        if checksum == data[3]:
            # Checksum matches, save the strain info
            low_byte = data[1]
            high_byte = data[2]
            try:
                strain.append(high_byte * 256 + low_byte)
            except IndexError:
                print("index error")
                pass
    # ser.close()             # close port
    print(strain)
    return (strain)


def main():
    i = 0
    df = pd.DataFrame()
    while i < 1000:
        output = read_strain("/dev/cu.usbmodem14201", 9600)
        output = pd.DataFrame(output)

        # df.append(output, ignore_index=True)
        df = pd.concat([df, output])

        i += 1

    df.to_csv("strain.csv", index=False)


if __name__ == "__main__":
    main()
