# scc_client.py

# This code requires scc.ino to be loaded into the Arduino

import serial
import time

# Edit these values based on the max coordinates in whatever system we use
MAX_X_COORD = 100
MAX_Y_COORD = 100

# For some ungodly reason, isdigit & isnumeric aren't working, so this is my crappy implementation
def isNum(c):
    if c == '0' or c == '1' or c == '2' or c == '3' or c == '4' or c == '5' or c == '6' or c == '7' or c == '8' or c == '9':
        return True

    return False

# Get user input COM port. Note that this cannot handle COM ports 10 or greater (if those exist)
cleared = False
while not cleared:
    PORT = input("Enter the port the Arduino is connected to (e.g. COM3)\n")
    portCheck = "COM"
    if len(PORT) == 4 and portCheck in PORT and isNum(PORT[3]):
        cleared = True
    else:
        print("'" + PORT + "' is not a valid port, try again...")

print("\nAttempting to establish a connection on port '" + PORT + "'")

arduino = serial.Serial(port=PORT, baudrate=9600, timeout=.1)

# We may need to write and immediately read a response, depending on the application
def write_read(x):
    if x[-1] != '\n':
        x += '\n'
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

# Process user input to see if it is in the format 'x,y' with max values of 100
def check_input(input):

    # Error catch (input must be at least 3 chars to be a coord)
    if len(input) < 3:
        return False

    if input[-1] != '\n':
        input += '\n'

    xcounter = 0

    # Count the number of digits from the start of the input until a non-digit character is reached
    while isNum(input[xcounter]):
        xcounter+=1
    
    if xcounter < 1:
        return False

    xcoord = input[:(xcounter)]
    print("X coord: " + xcoord)
    # If the non-digit character is not a ',' or the value is greater than 100, return false
    if input[xcounter] != "," or int(xcoord) > MAX_X_COORD:
        return False

    # Do the same for the y coordinate
    ycounter = xcounter + 1
    while isNum(input[ycounter]):
        ycounter+=1
    
    if ycounter == (xcounter + 1):
        return False

    ycoord = input[(xcounter + 1):ycounter]
    print("Y coord: " + ycoord)
    if input[ycounter] != '\n' or int(ycoord) > MAX_Y_COORD:
        return False

    return True
    

    


# Loop where the user enters coordinates (may change in the future to use a file instead)
while True:

    coord = input("Enter a coordinate (format 'x,y'), or 'quit' to exit\n") # Taking input from user
    if coord == "exit" or coord == "quit":
        break
    
    if check_input(coord):
        # TEST
        #print("Input " + coord + " is considered valid.")
        value = write_read(coord)
        print(value) # printing the value
    else:
        print("\n'" + coord + "' is not a valid coordinate. Try again...")
    
    

print("Closing connection on port " + PORT)
print("Please unplug the arduino before running the code again")
arduino.close()