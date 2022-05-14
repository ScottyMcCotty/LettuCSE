
// PINS FOR AGGIE DEMO BUTTONS; instantiate with correct pins in lab before running!
const int UP_BTN_PIN= A0;
const int DWN_BTN_PIN = A1;

const int FORKLIFT_TRAY_LIMIT = 9; // limit switch X: fork has been lowered to maximum
const int FORKLIFT_ARM_LIMIT = 10; // limit switch Y: fork has been lowered to tray
const int FORKLIFT_TOP_LIMIT = 11; // limit switch Z: forklift has been raised to maximum

// these are the pins when the driver is plugged into X
const int STEP_PIN = 2;
const int DIR_PIN = 5;

const int half_period = 700;
//const int NUM_EXTRA_STEPS = 50;

const String UP = "0";
const String DOWN = "1";
//const String CALIBRATION_STRING = "calibrate";

//const int TOOLHEAD_TRAVEL = 1000; // 2000 motor steps ~ 80 mm

bool debug = true;

void setup() {
  // pinMode setup
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);

  pinMode(FORKLIFT_ARM_LIMIT, INPUT_PULLUP);
  pinMode(FORKLIFT_TOP_LIMIT, INPUT_PULLUP);
  pinMode(FORKLIFT_TRAY_LIMIT, INPUT_PULLUP);

  // Aggie demo button setup
  pinMode(UP_BTN_PIN, INPUT_PULLUP);
  pinMode(DWN_BTN_PIN, INPUT_PULLUP);
  
  Serial.begin(115200);
  delay(500);
  
  //Serial.println("Hello, world!");
}

void loop() {
  
  //String input = wait_for_input("Toolhead command? ");

  // Aggie demo loop does not require command inputs; simply poll buttons

  // Move up or down while appropriate button is held. If both held at once, default to up
  if (digitalRead(UP_BTN_PIN) == LOW) {
    // Only move up if the button is held AND the upper limit switch isn't triggered
    if (debug) Serial.println("Going upp!");
    digitalWrite(DIR_PIN, LOW);
    while ((digitalRead(UP_BTN_PIN) == LOW) && (digitalRead(FORKLIFT_TOP_LIMIT) == HIGH)) {
      // Move up (code copypasted from auto_calibrate)
      digitalWrite(STEP_PIN, HIGH);
      delayMicroseconds(half_period);
      digitalWrite(STEP_PIN, LOW);
      delayMicroseconds(half_period);
    }
    if (debug) {
      Serial.println(digitalRead(FORKLIFT_TOP_LIMIT));
    }
  }
  if (digitalRead(DWN_BTN_PIN) == LOW){
    // Only move down if the button is held & NEITHER of the lower limit switches are triggered
    if (debug) Serial.println("Going downnnn");
    digitalWrite(DIR_PIN, HIGH);
    while ((digitalRead(DWN_BTN_PIN) == LOW) && (digitalRead(FORKLIFT_ARM_LIMIT) == HIGH)
            && (digitalRead(FORKLIFT_TRAY_LIMIT) == HIGH)){
      // Move down (code copypasted from toolhead_down)
      digitalWrite(STEP_PIN, HIGH);
      delayMicroseconds(half_period);
      digitalWrite(STEP_PIN, LOW);
      delayMicroseconds(half_period);
    }
    if (debug) {
      Serial.print(digitalRead(FORKLIFT_ARM_LIMIT)); Serial.print(" && "); Serial.println(digitalRead(FORKLIFT_TRAY_LIMIT));
    }
  }
  

  /*if (input == CALIBRATION_STRING) {
    auto_calibrate();
    
  } else if (input == UP) {
    toolhead_up();
    
  } else if (input == DOWN) {
    toolhead_down();
    
  } else {
    Serial.println("Failed! Unknown command");
    // block forever
    while(1){}
    
  }*/
  
}

// move toolhead up towards the top limit switch
void auto_calibrate() {

  digitalWrite(DIR_PIN, LOW);
  while (digitalRead(FORKLIFT_TOP_LIMIT) == HIGH) {
    // motor hasn't been triggered yet, keep rolling in positive direction
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(half_period);
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(half_period);
  }

  Serial.println("Calibrated");
  // we can say this is the home position
  // Barely just in front of triggering the limit switch
}

/*
 * Scott's function move_blocking(int motor_step_pin, int motor_direction_pin, int num_steps, int dir, int half_step_delay)
 * 
 * This function runs the specified motor the specified number of steps before returning to the caller.
 * It essentially blocks the rest of the program from execution until it has finished, so this function
 * DOES NOT SUPPORT SIMULTANEOUS MOTOR MOVEMENT. This means we'll probably want to not use this when we have limit switches
 * and/or safety checks to stop the movement mid-command.
 * 
 * motor_step_pin: the steps pin which the motor is attached to via CNC shield (should be STEP_PIN)
 * motor_direction_pin: the direction pin which the motor is attached to via CNC shield (should be DIR_PIN)
 * num_steps: the number of pulses to send to the motor. 200 steps per revolution
 * dir: the direction to spin motor. See frame for positive/negative labels
 * half_step_delay: the delay (in microseconds) between each high and low write, equalling half the period of a pulse
 * 
 * Return: None
 */
//void move_blocking(int motor_step_pin, int motor_direction_pin, int num_steps, int dir, int half_step_delay) {
//  // set direction
//  digitalWrite(motor_direction_pin, dir);
//
//  // apply movement
//  for(int ii = 0; ii < num_steps; ii++) {
//    digitalWrite(motor_step_pin, HIGH);
//    delayMicroseconds(half_step_delay);
//    digitalWrite(motor_step_pin, LOW);
//    delayMicroseconds(half_step_delay);
//  }
//}


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

    // check for naughty things here
    if (digitalRead(FORKLIFT_TOP_LIMIT) == LOW) {
      // hit the top, end early
      return;
    }

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


// Pause until input (terminated with \n) is received
String wait_for_input(String prompt) {
  int state = 0;
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
    move_not_blocking(STEP_PIN, DIR_PIN, LOWERED_MOVEMENT, dir(LOWERED_MOVEMENT), half_period);
    positionDown = true;
    //Serial.println("Done");
  } else { // move to raised position
    move_not_blocking(STEP_PIN, DIR_PIN, RAISED_MOVEMENT, dir(RAISED_MOVEMENT), half_period);
    positionDown = false;
    //Serial.println("Done");
  }

  Serial.println("Done");
}*/

// Move toolhead up by TOOLHEAD_TRAVEL motor steps.
//void toolhead_up() {
//  move_not_blocking(STEP_PIN, DIR_PIN, TOOLHEAD_TRAVEL, LOW, half_period);
//  Serial.println("Done");
//}

// Move toolhead down by TOOLHEAD_TRAVEL motor steps.
//void toolhead_down() {
//  move_not_blocking(STEP_PIN, DIR_PIN, TOOLHEAD_TRAVEL, dir(-1), half_period);
//  Serial.println("Done");
//}

// Move toolhead down until it hits the limit switch.
//void toolhead_down() {
//
//  bool moved = false;
//  // set direction negative
//  digitalWrite(DIR_PIN, HIGH);
//  while (digitalRead(FORKLIFT_ARM_LIMIT) == HIGH) {
//    // motor hasn't been triggered yet, keep rolling in negative direction
//    moved = true;
//    digitalWrite(STEP_PIN, HIGH);
//    delayMicroseconds(half_period);
//    digitalWrite(STEP_PIN, LOW);
//    delayMicroseconds(half_period);
//  }
//
////  delay(500);
//
//  // if the motor was moved down, give it a few more steps
//  // to ensure that it's low enough
//  if (moved) {
//    for (int ii = 0; ii < NUM_EXTRA_STEPS; ++ii) {
//      digitalWrite(STEP_PIN, HIGH);
//      delayMicroseconds(half_period);
//      digitalWrite(STEP_PIN, LOW);
//      delayMicroseconds(half_period);
//    }
//  }
//  Serial.println("Done");
//}
