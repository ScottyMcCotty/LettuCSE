

/*
 * This code is meant to be uploaded to the frame controller and interacted with via the arduino IDE serial monitor
 */


// Stepper Motor X
const int X_STEP_PIN = 2;
const int X_DIR_PIN = 5;
//const int Y_STEP_PIN = 3;
//const int Y_DIR_PIN = 6;
const int Z_STEP_PIN = 4;
const int Z_DIR_PIN = 7;

//const int PULSE_DUR = 500;  // Duration of each pulse
//const int NUM_STEPS = 8100; // Not used?

const int BUFFER_SIZE = 20;

int X_MOTOR_POS = 4000;
int Z_MOTOR_POS = 2800;
 
void setup() {
  // Sets the two pins as Outputs
  pinMode(X_STEP_PIN, OUTPUT); 
  pinMode(X_DIR_PIN, OUTPUT);
  pinMode(Z_STEP_PIN, OUTPUT); 
  pinMode(Z_DIR_PIN, OUTPUT);
  
  Serial.begin(9600);
  Serial.setTimeout(2000);

  wait_for_input();

  Serial.println("Setup finished");

  move_blocking(Z_STEP_PIN, Z_DIR_PIN, 200, LOW, 500);
  delay(200);
  move_blocking(Z_STEP_PIN, Z_DIR_PIN, 200, HIGH, 500);
}

void loop() {

//  delay(1000);
//  Serial.println("Loop is running");

  String input = wait_for_input();

  String distance = input.substring(2);
  int steps = distance.toInt();
  int dir = HIGH;
  if (steps < 0) dir = LOW;
  steps = abs(steps);

  Serial.print("Moving motor "); Serial.print(input[0]); Serial.print(steps); Serial.print(" in direction "); Serial.println(dir);
  
  if (input[0] == 'X') {
    move_blocking(X_STEP_PIN, X_DIR_PIN, steps, dir, 500);
  }
  else {
    move_blocking(Z_STEP_PIN, Z_DIR_PIN, steps, dir, 500);
  }
  
}

/*
 * function wait_for_input()
 * 
 * This function blocks until any input is received over Serial connection.
 * The input is then returned to the caller as a string.
 * DELIMITED BY '\n' CHARACTER
 * 
 * Return: String
 */
String wait_for_input() {
  int state = 0;
  int count = 0;
//  char buf[BUFFER_SIZE];

  char buf[10] = {'\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0'};
  
  while (state == 0) {
    Serial.print("Waiting to start... send any key ("); Serial.print(++count); Serial.println(")");
    state = Serial.readBytesUntil('\n', buf, BUFFER_SIZE);
  }

  Serial.print("Received input: '"); Serial.print(buf); Serial.println("'");

  return String(buf);
}


/*
 * function move_blocking(int motor_step_pin, int motor_direction_pin, int num_steps, int dir, int half_step_delay)
 * 
 * This function runs the specified motor the specified number of steps before returning to the caller.
 * It essentially blocks the rest of the program from execution until it has finished, so this function
 * DOES NOT SUPPORT SIMULTANEOUS MOTOR MOVEMENT
 * 
 * motor_step_pin: the steps pin which the motor is attached to via CNC shield
 * motor_direction_pin: the direction pin which the motor is attached to via CNC shield
 * num_steps: the number of pulses to send to the motor. 200 steps per revolution
 * dir: the direction to spin motor. See frame for positive/negative labels
 * half_step_delay: the delay (in microseconds) between each high and low write, equalling half the period of a pulse
 * 
 * Return: None
 */
void move_blocking(int motor_step_pin, int motor_direction_pin, int num_steps, int dir, int half_step_delay) {
  
  // set direction
  digitalWrite(motor_direction_pin, dir);

  // do movement
  for (int ii = 0; ii < num_steps; ii++) {
    digitalWrite(motor_step_pin, HIGH);
    delayMicroseconds(half_step_delay);
    digitalWrite(motor_step_pin, LOW);
    delayMicroseconds(half_step_delay);
  }
}
