# Test API

This code is meant to act as a way to test whether a client is capable of sending Serial messages to an Arduino device.

At the time of writing this documentation, the Arduino has control of two LEDs.

## Arduino API:
* `red` turns on the red light for one second
* `blue` turns on the blue light for one second
* `purple` turns on both lights for one second
* Any other command will send an error message response

The commands must have `\n` following them, in order for the Arduino to recognize the end of a command.

Otherwise the poor thing might think every letter is a command.

THIS IS A SOFTWARE CHOICE, NOT PART OF THE HARDWARE. We could use any character to delimit commands, but `\n` makes the most sense
because the Arduino IDE sends a newline character by default when you press `enter` after typing something in the Serial monitor.

For instructions on **How to interact with an Arduino that already has code on it**, please read `Arduino_Code/README.md`

## Defining Success:

As always, it's import to define what a successful test will look like. 
I would consider the API to be successfully and fully tested when each of the light patterns are able to be made by a client program:
* Blinking red
* Blinking blue
* Blinking purple
* Alternating red and blue blinks
* Continuously keeping red on
* Continuously keeping red on while blinking blue

Keep in mind, each time the Arduino receives a color command it will keep the related LED on for only the next second.

I'd suggest looking for a Serial communication library for Python.

... see README.md in Arduino_Code folder for Python serial communication
