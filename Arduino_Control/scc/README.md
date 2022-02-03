# Test API

This code is meant to send basic commands that resemble coordinates to the Arduino and see if it recognizes them in turn.
'scc.ino' should be flashed to the Arduino, and 'scc_client.py' should be run on the desktop the Arduino is connected to.

## scc_client API:

The Python program should ask for the proper port to connect to the Arduino (e.g. COM3), and provide a basic catch & retry
if the user inputs something else (e.g. only input in the format of 'COMx" where X is a number should pass).

Once it has passed, it should enter a loop where it asks for coordinates in the format of 'x,y' while imposing a maximum limit
on each value (set to 100). It will send these coordinates as one command to the Arduino in the same format (e.g. '3,25').
If the user inputs something invalid (e.g. any letters, a coordinate greater than the maximum limit, or the command isn't in the
'x,y' format), catch & retry. If the user inputs 'quit' or 'exit', terminate.

## Arduino API:

At the time of writing this documentation, the Arduino has control of two LEDs.
It should take the input (format 'x,y' expected) and parse it:

* the red LED should blink 'x' number of times, ideally switching on and off every 0.25s for a full loop in half a second
* the blue LED should blink 'y' number of times at the same rate as the red LED, after the red LED is done blinking

For example, an input of '5,3' should have the red LED blinking 5 times and the blue LED blinking 3 times.

Obviously, in the future the command will do far more than just causing LEDs to blink, but if this works it proves
the interface between the Python program and the Arduino is sound.