
# this code works with copycat.ino and test_API.ino

import serial
import time

PORT = input("Enter port that arduino is connected to (ex: COM4)\n")
print("\nYou entered port '" + PORT + "', I sure hope that's correct")

arduino = serial.Serial(port=PORT, baudrate=9600, timeout=.1)

time.sleep(.6) # sleep for a second to give the setup the time it needs? IDK if that's even necessary but it feels safe

# We may need to write and immediately read a response, depending on the application
def write_read(x):
    if x[-1] != '\n':
        x += '\n'
    arduino.write(bytes(x, 'utf-8'))
    # arduino.write(x.encode('utf-8'))
    time.sleep(1.5)
    data = arduino.readline()
    return data

values = ["red", "blue", "purple"]
index = 0
count = 0

while count < 4*len(values):

    count += 1

    print("Writing: '" + values[index] + "'")
    ret = write_read(values[index])
    index = (index + 1) % len(values)
    print(ret) # printing the value
    print()

print("Closing connection on port " + PORT)
print("Please unplug the arduino before running the code again")
arduino.close()
