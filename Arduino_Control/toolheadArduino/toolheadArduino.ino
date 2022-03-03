// Global vars (NOTE: Pin values in particular may need changing based on arduino wiring in lab)

const int Y_STOP_PIN = 9;
const int Y_STEP_PIN = 2;
const int Y_DIR_PIN = 5;

const int half_period = 1100; // Unsure what this does but is called for calibrating

// If true (1), toolhead is extended downward. False (0) means toolhead is raised.
bool positionDown = false;


void setup() {
  // pinMode setup
  pinMode(Y_STEP_PIN, OUTPUT);
  pinMode(Y_DIR_PIN, OUTPUT);

  //TODO: unsure if stop pins are being used for toolhead
  pinMode(Y_STOP_PIN, INPUT_PULLUP);
  
  // Start the connection with baudrate = 115200 and a minor delay
  Serial.begin(115200)
  delay(500);

  //TODO: Call calibration function if needed
  //calibrate();
}

void loop() {
  // Continue after receiving input
  int input = wait_for_input("Toolhead command? ").toInt();

  // Call the relevant movement commands based on input
  switch(input) {
    case 0: // release_plant: raise toolhead
      toolhead_move(false); // Should only be two binary positions, no specified coordinates needed
      break;
    case 1: // grab_plant: lower toolhead
      toolhead_move(true);
      break;
    default: // unrecognized command
      Serial.println("Error");
      break;
  }
}

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
// Set the "up" position by 

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

// TOOLHEAD MOVEMENT FUNCTION: 0 input means move to low position, 1 moves to high
void toolhead_move(bool movePos) {

  // Shouldn't ever try to move to the position it is already at
  if (movePos == positionDown) {
    Serial.println("Error");
    return;
  }

  // Move the motor based on the input direction
  if (movePos) { // move to lowered position
    //TODO: We don't know yet if lowering requires negative or positive movement. Will need to test in lab
    
    Serial.println("Down");
  } else { // move to raised position

    Serial.println("Up");
  }
}
