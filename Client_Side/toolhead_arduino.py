"""Module contains vertical arduino class"""
import time
from arduino import Arduino
from gui import GUI


class ToolheadArduino(Arduino):

    """
    A class to represent the Arduino being used to move the arm up and down,
    as well as open and close the cup device which drops or grabs the plant

    ...

    Attributes
    ----------
    mm_per_motor_step : int
        the number of milimeters the arm will move during each motor step
    arduinoConnection : serial
        the connection between the program and the Arduino
    serial_number : int
        the serial number of the arduino that is being used for the toolhead
        if you change the toolhead arduino you will have to change this number

    Methods
    -------
    __init__(mm_per_motor_step, gui):
        calls the parent init, and then lists the connected port in
        the toolhead arduino section of the GUI
    grab_plant():
        lowers the toolhead arm to the plant and grabs it
    release_plant():
        releases the plant and raises the toolhead arm
    """


    serial_number = 55838343733351510170


    def __init__(self, mm_per_motor_step:int, gui:GUI):
        '''
            Initialize the arduino and then list the name of the port connected to the
            arduino in the toolhead port label on the gui

            Parameters:
                    mm_per_motor_step : int
                        the number of milimeters the arm will move during each motor step
                    gui (GUI): the tkinter window object that everything is displayed on
            Returns:
                    None
        '''
        super().__init__(mm_per_motor_step, gui)
        if self.arduino_connection is None:
            gui.toolhead_arduino_label("Arduino not connected")
        else:
            gui.toolhead_arduino_label(self.arduino_port)
            super().wake_up()

    def release_plant(self):
        """opens the cup-grasp and lets the plant fall"""
        #actually signal arduino
        self.gui.update_status("Toolhead releasing plant")

        timeout = time.time() + 25 # 25s to timeout

        #sending a '2' to toolhead arduino signifies releasing->raising
        if self.arduino_connection:
            self.arduino_connection.write(bytes("2"), 'utf-8')
            while (True):
                value = self.arduino_connection.readline().decode("utf-8")
                if "Up" in value:
                    break
                if "Error" in value:
                    #TODO: throw unrecognized command error
                    break
                if time.time() > timeout:
                    #TODO: throw timeout error
                    break

        #make it so that rather than sleep you wait for a response
        #time.sleep(0.1)

    def grab_plant(self):
        """closes the cup-grasp to hold the plant"""
        #actually signal arduino
        self.gui.update_status("Toolhead grabbing plant")

        timeout = time.time() + 25 # 25s to timeout

        #sending a '1' to toolhead arduino signifies lowering->grabbing
        if self.arduino_connection:
            self.arduino_connection.write(bytes("1"), 'utf-8')
            while (True):
                value = self.arduino_connection.readline().decode("utf-8")
                if "Down" in value:
                    break
                if "Error" in value:
                    #TODO: throw unrecognized command error
                    break
                if time.time() > timeout:
                    #TODO: throw timeout error
                    break

        #make it so that rather than sleep you wait for a response
        #time.sleep(0.1)
