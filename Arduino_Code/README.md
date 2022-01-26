# Arduino Code

One of the quirks about arduino code is that it must be located in a folder with the same name as the code file.

For example, `foo.ino` needs to be in a `foo` folder.

Sometimes the comments in code aren't enough, so additional documentation for a specific `.ino` file should be placed in the related folder for that code.

# General Arduino Information

Download the Arduino IDE by using google. Easy enough

## Run code already on Arduino
Sometimes the Arduino already has code on it, and you just want to run the code in your Arduino IDE. Follow these steps:
1. Open the Arduino IDE with any code in it (probably an empty default sketch)
2. Plug in the arduino
3. Select port (probably COM 3 or 4)
4. Open the Serial Port Monitor (under the tools menu or something. There's also a shortcut button on the top right)
   1. NOTE: Opening the Serial Port Monitor restarts whatever code is on the arduino. This is usually a good thing
5. View the arduino sending Serial messages, or send your own Serial messages to the arduino
   1. Typically best to use `newline` as the delimiter

## Upload code onto Arduino
Sometimes you have Arduino code and want to upload it onto the Arduino. Follow these steps:
1. Open code `.ino` in Arduino IDE
2. Select board (probably Arduino UNO)
3. Press the check mark in IDE to confirm that code can compile
4. Plug in arduino
5. Select port (probably COM 3 or 4)
6. Press the arrow upload button

If you want to find out which port the Arduino is connected to, and for some reason the IDE isn't telling you,
open the device manager and check under the `Ports (COM & LPT)` section.

Apparently there's an Arduino extension for VS Code. Feel free to try it out, but all the instructions I've written are for the actual Arduino IDE.

UPDATE: I tried the extension and it didn't even fix all the syntax highlighting for my `.ino` file. I don't trust it...