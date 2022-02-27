
# this code works with doubler.ino and copycat.ino

import serial
import time

PORT = input("Enter port that arduino is connected to (ex: COM4)\n")
print("\nYou entered port '" + PORT + "', I sure hope that's correct")

arduino = serial.Serial(port=PORT, baudrate=9600, timeout=.1)

# We may need to write and immediately read a response, depending on the application
def write_read(x):
    if x[-1] != '\n':
        x += '\n'
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

while True:

    num = input("Enter a number: ") # Taking input from user
    if num == "exit":
        break
    value = write_read(num)
    print(value) # printing the value

print("Closing connection on port " + PORT)
print("Please unplug the arduino before running the code again")
arduino.close()
