
from json import tool
from time import sleep
from serial import Serial, SerialException
from serial.tools import list_ports

def move_arduino(arduino: Serial, command: str) -> str:

    # in case someone forgets to add a newline on their command:
    if command[-1] != "\n":
        command = command + "\n"

    arduino.write(bytes(command, "utf-8"))

    while True:

        response = arduino.readline().decode("utf-8")

        if response == "":
            print("Waiting for response...")
            sleep(.5)
        else:
            print(f"Response: '{response}'!")
            return response



#* Frame serial number
frame_serial = "957363235323514040C0"
frame_connection = None

#* Toolhead serial number
toolhead_serial = "957363235323515012A2"
toolhead_connection = None

for port in list_ports.comports():

    # print("Testing port", port.name)

    if str(frame_serial) == str(port.serial_number):
        print("Found the port with the FRAME arduino")
        try:
            frame_connection = Serial(port.device, baudrate=9600, timeout=.1)
        except SerialException:
            print("Connection failed:", port.name)
    elif str(toolhead_serial) == str(port.serial_number):
        print("Found the port with the TOOLHEAD arduino")
        try:
            toolhead_connection = Serial(port.device, baudrate=9600, timeout=.1)
        except SerialException:
            print("Connection failed:", port.name)
    else:
        print(port.serial_number, "doesn't match one we need")

# exit()
# sleep(3) # let the arduinos get booted up and whatnot

while True:
    msg = toolhead_connection.readline().decode("utf-8")
    if msg == "":
        print("Waiting for toolhead's initial message")
    else:
        print("Toolhead's initial message:")
        print(msg)
        break

while True:
    msg = frame_connection.readline().decode("utf-8")
    if msg == "":
        print("Waiting for frame's initial message")
    else:
        print("Frame's initial message:")
        print(msg)
        break


# move_arduino(frame_connection, "300 300\n")
# move_arduino(toolhead_connection, "1\n")
# move_arduino(toolhead_connection, "0\n")
# move_arduino(frame_connection, "0 0\n")


move_arduino(toolhead_connection, "1\n")

move_arduino(frame_connection, "-175, 0\n")

sleep(2)

move_arduino(toolhead_connection, "0\n")

move_arduino(frame_connection, "-175, 380\n")

move_arduino(toolhead_connection, "1\n")

# sleep(2)

move_arduino(frame_connection, "20, 380\n")

move_arduino(toolhead_connection, "0\n")

move_arduino(frame_connection, "0, 0\n")



frame_connection.close()
toolhead_connection.close()
