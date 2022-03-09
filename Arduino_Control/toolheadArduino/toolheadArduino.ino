// Global vars (NOTE: Pin values in particular may need changing based on arduino wiring in lab)

const int Y_STOP_PIN = 9;

//const int Y_STEP_PIN = 3;
//const int Y_DIR_PIN = 6;

// Keeping it called Y_STEP_PIN even though
// it ain't plugged into the 
const int Y_STEP_PIN = 2;
const int Y_DIR_PIN = 5;

const int half_period = 1100;

const int TOOLHEAD_TRAVEL = 1000; // 2000 motor steps ~ 80 mm

//const int RAISED_MOVEMENT   = 1000;  // Number of motor steps to go from lowered to raised position
//const int LOWERED_MOVEMENT  = -1000; // Number of motor steps to go from raised to lowered position

// If true (1), toolhead is extended downward. False (0) means toolhead is raised. Toolhead assumed to start raised.
bool positionDown = false;

#define dir(x) ((x) < 0 ? LOW : HIGH)


void setup() {
  // pinMode setup
  pinMode(Y_STEP_PIN, OUTPUT);
  pinMode(Y_DIR_PIN, OUTPUT);

  //TODO: unsure if stop pins are being used for toolhead
  // ^ they're not yet -Scott
//  pinMode(Y_STOP_PIN, INPUT_PULLUP);
  
  // Start the connection with baudrate = 115200 and a minor delay
  Serial.begin(115200);
  delay(500);

  //TODO: Call calibration (or autocalibrate) function if needed
  //calibrate();
//  auto_calibrate(Y_STEP_PIN, Y_DIR_PIN, Y_STOP_PIN);
}

void loop() {
  // Continue after receiving input
  int input = wait_for_input("Toolhead command? ").toInt();

  // Call the relevant movement commands based on input
  switch(input) {
    case 0: // release_plant: raise toolhead
//      toolhead_move(false); // Should only be two binary positions, no specified coordinates needed
      toolhead_down();
      break;
    case 1: // grab_plant: lower toolhead
//      toolhead_move(true);
      toolhead_up();
      break;
    default: // unrecognized command
      Serial.println("Error");
      while(1){}
      break;
  }

  // FOR TESTING PURPOSES ONLY
  // if input is between -1000 and 1000, call test movement function
//  if ((input <= 1000 || input >= -1000) && (input != 0 && input != 1)) {
//    test_custom_move(input);
//  }

  Serial.println("Done");
}

// TEST FUNCTION ONLY
// Send a custom amount of motor steps to the toolhead.
//void test_custom_move(int steps) {
//  move_not_blocking(Y_STEP_PIN, Y_DIR_PIN, steps, dir(steps), half_period);
//  Serial.println("Done");
//}

// MANUAL Calibrate:  Set the "up" position for the toolhead manually by
//                    inputting motor movements until position is satisfactory
void calibrate() {
  Serial.print("Calibrating toolhead pin "); Serial.println(Y_STEP_PIN);
  Serial.println("Enter integer, or 'save'");

  while (true) {
    String input = wait_for_input("Relative movement, single axis? ");

    if (input == "save") break;
  
    int steps = input.toInt();
    int dir = (steps < 0) ? LOW : HIGH;
    steps = abs(steps);

    // Move the toolhead via the blocking function. Nothing else can run until this movement completes
    move_blocking(Y_STEP_PIN, Y_DIR_PIN, steps, dir, half_period);
  }
}

// AUTO Calibrate (requires limit switches installed):
// Set the "up" position by moving up until a limit switch is hit.
// Note this function is currently not called at all. Revisit when limit switches installed.

//TODO: Unsure if this code calibrates by moving up into the raised position, or if it moves down.
//      Needs testing in lab once limit switches are installed
void auto_calibrate(int motor_pin, int dir_pin, int stop_pin) {
  //Serial.print("Auto-calibrating pin "); Serial.println(motor_pin);
  // Serial.println("Enter integer, or 'save'");

  // set direction positive
  digitalWrite(dir_pin, HIGH);
  while (digitalRead(stop_pin) == HIGH) {
    // motor hasn't been triggered yet, keep rolling in positive direction
    digitalWrite(motor_pin, HIGH);
    delayMicroseconds(half_period);
    digitalWrite(motor_pin, LOW);
    delayMicroseconds(half_period);
//    Serial.println("Moving negative");
//    delay(200);
  }

  delay(500);

  // we ran into the limit switch, now we want to back off a bit until it's not being touched
  digitalWrite(dir_pin, LOW);
  while(digitalRead(stop_pin) == LOW) {
    // move it slowly away from the limit switch
    digitalWrite(motor_pin, HIGH);
    delayMicroseconds(half_period * 2);
    digitalWrite(motor_pin, LOW);
    delayMicroseconds(half_period * 2);
//    Serial.println("Moving positive");
//    delay(200);
  }

  //Serial.println("Calibrated.");
  // we can say this is the home position. Barely just in front of triggering the limit switch
}

/*
 * Scott's function move_blocking(int motor_step_pin, int motor_direction_pin, int num_steps, int dir, int half_step_delay)
 * 
 * This function runs the specified motor the specified number of steps before returning to the caller.
 * It essentially blocks the rest of the program from execution until it has finished, so this function
 * DOES NOT SUPPORT SIMULTANEOUS MOTOR MOVEMENT. This means we'll probably want to not use this when we have limit switches
 * and/or safety checks to stop the movement mid-command.
 * 
 * motor_step_pin: the steps pin which the motor is attached to via CNC shield (should be Y_STEP_PIN)
 * motor_direction_pin: the direction pin which the motor is attached to via CNC shield (should be Y_DIR_PIN)
 * num_steps: the number of pulses to send to the motor. 200 steps per revolution
 * dir: the direction to spin motor. See frame for positive/negative labels
 * half_step_delay: the delay (in microseconds) between each high and low write, equalling half the period of a pulse
 * 
 * Return: None
 */
void move_blocking(int motor_step_pin, int motor_direction_pin, int num_steps, int dir, int half_step_delay) {
  // set direction
  digitalWrite(motor_direction_pin, dir);

  // apply movement
  for(int ii = 0; ii < num_steps; ii++) {
    digitalWrite(motor_step_pin, HIGH);
    delayMicroseconds(half_step_delay);
    digitalWrite(motor_step_pin, LOW);
    delayMicroseconds(half_step_delay);
  }
}

// Movement function, but this version doesn't block the rest of the program from executing.
// Allows for mid-movement interruption, for limit switches or safety shutoffs for example
void move_not_blocking(int motor_step_pin, int motor_direction_pin, int num_steps, int dir, int half_step_delay) {

  // Double the number of steps since we're moving in half-steps
  num_steps = num_steps * 2;

  // set direction
  digitalWrite(motor_direction_pin, dir);

  // setup for movement
  int counter = 0;
  unsigned long othercounter = 0; // Doesn't seem to be used at all?
  int pulse = HIGH;
  unsigned long previous = micros();

  while (counter < num_steps) {
    unsigned long current = micros();

    if (current - previous > half_step_delay) {
      digitalWrite(motor_step_pin, pulse);
      pulse = (pulse + 1) % 2;
      previous = current;
      counter++;
    } else {
      othercounter++;
    }
  }
}

// Scott's (cleaned up) function to pause until input (terminated with \n) is received
String wait_for_input(String prompt) {
  int state = 0;
  int count = 0;
  char buf[] = {'\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0',
                '\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0'};

  while (state == 0) {
    state = Serial.readBytesUntil('\n', buf, 20);
  }

  return String(buf);
}

// TOOLHEAD MOVEMENT FUNCTION: true input means move to low position, false moves to raised
/*void toolhead_move(bool movePos) {

  // Move the motor based on the input direction
  if (movePos) { // move to lowered position
    //TODO: We don't know yet if lowering requires negative or positive movement. Will need to test in lab
    move_not_blocking(Y_STEP_PIN, Y_DIR_PIN, LOWERED_MOVEMENT, dir(LOWERED_MOVEMENT), half_period);
    positionDown = true;
    //Serial.println("Done");
  } else { // move to raised position
    move_not_blocking(Y_STEP_PIN, Y_DIR_PIN, RAISED_MOVEMENT, dir(RAISED_MOVEMENT), half_period);
    positionDown = false;
    //Serial.println("Done");
  }

  Serial.println("Done");
}*/

// Move toolhead up by TOOLHEAD_TRAVEL motor steps.
void toolhead_up() {
  move_not_blocking(Y_STEP_PIN, Y_DIR_PIN, TOOLHEAD_TRAVEL, dir(1), half_period);
  positionDown = false;
//  Serial.println("Done");
}

// Move toolhead down by TOOLHEAD_TRAVEL motor steps.
void toolhead_down() {
  move_not_blocking(Y_STEP_PIN, Y_DIR_PIN, TOOLHEAD_TRAVEL, dir(-1), half_period);
  positionDown = false;
//  Serial.println("Done");
}

// Move toolhead down until it hits the limit switch.
//void toolhead_down() {
//  // set direction negative
//  digitalWrite(Y_DIR_PIN, LOW);
//  while (digitalRead(Y_STOP_PIN) == HIGH) {
//    // motor hasn't been triggered yet, keep rolling in negative direction
//    digitalWrite(Y_STEP_PIN, HIGH);
//    delayMicroseconds(half_period);
//    digitalWrite(Y_STEP_PIN, LOW);
//    delayMicroseconds(half_period);
////    Serial.println("Moving negative");
////    delay(200);
//  }
//
//  //TODO: Should there be a failsafe if the limit switch is never hit?
//
//  Serial.println("Done");
//}
