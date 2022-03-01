

// define pin constants
#define RED_PIN 8
#define BLUE_PIN 2
#define DELAY_DURATION 500
#define ON_DURATION 500

long red_start_time = 0;
long blue_start_time = 0;
bool string_complete = false;
bool red_is_on = false;
bool blue_is_on = false;
String input = "";

int xcoord = -1;
int xcounter = -1;
int ycoord = -1;
int ycounter = -1;
bool command_in_progress = false;
bool red_cycle_in_progress = false;
bool blue_cycle_in_progress = false;

void setup() {
  // do nothing
  Serial.begin(9600);
  pinMode(RED_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  //delay(50);
  //Serial.println("Valid client instructions:\n  red\n  blue\n  purple\n");
}

void loop() {

  if (string_complete && !command_in_progress) {
    string_complete = false;

    xcounter = 0;
    ycounter = 0;

    // Get the x coord and y coord from the input (limit of 5 is a safety catch)
    while (input.substring(xcounter, xcounter + 1) != "," && xcounter <= 5) {
      xcounter++;
    }
    xcoord = input.substring(0, xcounter).toInt();
    ycoord = input.substring(xcounter + 1).toInt();

    //Serial.println("xcoord is " + String(xcoord) + ", ycoord is " + String(ycoord) + "!");

    // Command is now executing so ignore further input until it is complete
    command_in_progress = true;
    
    /*
    if (input == "red") {
      redOn();
      red_start_time = millis();
    }
    else if (input == "blue") {
      blueOn();
      blue_start_time = millis();
    }
    else if (input == "purple") {
      purpleOn();
      red_start_time = millis();
      blue_start_time = millis();
    }
    else {
      Serial.println("What are you doing? '" + input + "' isn't a known command");
    }*/

    // reset the input string
    input = "";
  }

  // If red LED is not cycling but it should be, start it up
  // NOTE: This decrements xcoord which will not work in the future
  if (xcoord > 0 && !red_cycle_in_progress) {
    xcoord--;
    red_cycle_in_progress = true;
    setRed(true);
    red_start_time = millis();
  }
  if (ycoord > 0 && !blue_cycle_in_progress) {
    ycoord--;
    blue_cycle_in_progress = true;
    setBlue(true);
    blue_start_time = millis();
  }
  // If LED has been on for half of ON_DURATION, turn it off but keep the cycle going
  if (red_is_on && millis() - red_start_time >= (ON_DURATION / 2)) {
    setRed(false);
  }
  if (blue_is_on && millis() - blue_start_time >= (ON_DURATION / 2)) {
    setBlue(false);
  }
  // If LED timer has passed ON_DURATION, cycle is complete
  if (red_cycle_in_progress && millis() - red_start_time >= ON_DURATION) {
    red_cycle_in_progress = false;
  }
  if (blue_cycle_in_progress && millis() - blue_start_time >= ON_DURATION) {
    blue_cycle_in_progress = false;
  }

  // If xcoord and ycoord are exhausted, end the command
  if (xcoord <= 0 && ycoord <= 0) {
    command_in_progress = false;
  }
  /*
  if (red_is_on && millis() - red_start_time >= ON_DURATION) {
    redOff();
    Serial.println("Success. Red LED now off");
  }
  if (blue_is_on && millis() - blue_start_time >= ON_DURATION) {
    blueOff();
    Serial.println("Success. Blue LED now off");
  }*/


// just testing the functions

//  redOn();
//  delay(DELAY_DURATION);
//  
//  redOff();
//  delay(DELAY_DURATION);
//
//  blueOn();
//  delay(DELAY_DURATION);
//
//  blueOff();
//  delay(DELAY_DURATION);
//
//  purpleOn();
//  delay(DELAY_DURATION);
//
//  purpleOff();
//  delay(DELAY_DURATION);
}

// Methods for manipulating LEDs
void setRed(bool set) {
  if (set) {
    digitalWrite(RED_PIN, HIGH);
    red_is_on = true;
  }
  else {
    digitalWrite(RED_PIN, LOW);
    red_is_on = false;
  }
}

void setBlue(bool set) {
  if (set) {
    digitalWrite(BLUE_PIN, HIGH);
    blue_is_on = true;
  }
  else {
    digitalWrite(BLUE_PIN, LOW);
    blue_is_on = false;
  }
}
/*
  SerialEvent occurs whenever a new data comes in the hardware serial RX. This
  routine is run between each time loop() runs, so using delay inside loop can
  delay response. Multiple bytes of data may be available.
*/
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      string_complete = true;
    }
    else {
      // otherwise, add it to the inputString:
      input += inChar;
    }
  }
}

void redOn() {
  // turn red LED on
  digitalWrite(RED_PIN, HIGH);
  red_is_on = true;
}

void redOff() {
  // turn red LED off
  digitalWrite(RED_PIN, LOW);
  red_is_on = false;
}

void blueOn() {
  // turn blue LED on
  digitalWrite(BLUE_PIN, HIGH);
  blue_is_on = true;
}

void blueOff() {
  // turn blue LED off
  digitalWrite(BLUE_PIN, LOW);
  blue_is_on = false;
}

void purpleOn() {
  // turn red and blue LEDs on
  redOn();
  blueOn();
}

void purpleOff() {
  // turn red and blue LEDs off
  redOff();
  blueOff();
}
