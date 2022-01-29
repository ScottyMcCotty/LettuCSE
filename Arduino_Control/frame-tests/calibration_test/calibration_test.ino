



const int X_STEP_PIN = 2;
const int X_DIR_PIN = 5;
const int Z_STEP_PIN = 4;
const int Z_DIR_PIN = 7;

int current_x = -1;
int current_y = -1;

const int half_period = 1200;

#define dir(x) ((x) < 0 ? LOW : HIGH)

void setup() {

  Serial.begin(9600);

  calibrate_axis(X_STEP_PIN, X_DIR_PIN);
  calibrate_axis(Z_STEP_PIN, Z_DIR_PIN);

  current_x = 0;
  current_y = 0;
  Serial.println("Home has been set!\nAbsolute coordinate mode activated");

}

void loop() {
  
  String input = wait_for_input("absolute move");

  int space = input.indexOf(" ");
  String x = input.substring(0, space);
  String y = input.substring(space+1);

  move_coordinates(x.toInt(), y.toInt());
//  Serial.println(x);
//  Serial.println(y);
  
}


void calibrate_axis(int motor_pin, int dir_pin) {
  Serial.print("Calibrating pin "); Serial.println(motor_pin);
  Serial.println("Enter integer, or 'save'");

  while (true) {
    String input = wait_for_input("move");

    if (input == "save") break;
  
    int steps = input.toInt();
    int dir = (steps < 0) ? LOW : HIGH;
    steps = abs(steps);
  
    move_blocking(motor_pin, dir_pin, steps, dir, half_period);
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
String wait_for_input(String prompt) {
  int state = 0;
  int count = 0;

  char buf[10] = {'\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0'};
  
  while (state == 0) {
//    Serial.print("Waiting to " + prompt + " ("); Serial.print(++count); Serial.println(")");
    state = Serial.readBytesUntil('\n', buf, 10);
  }

  Serial.print("Received input: '"); Serial.print(buf); Serial.println("'");

  return String(buf);
}


/*
 * function move_coordinates(int x, int y)
 * 
 * This function moves the toolhead to the designated x,y coordinates, which requires having 0,0 being set.
 * It uses the move_blocking function for relative movements
 * 
 * x: the new x position for the toolhead
 * y: the new y position for the toolhead
 * 
 * Return: None
 */
void move_coordinates(int x, int y) {

  if (current_x == -1 || current_y == -1) {
    return;
  }

  Serial.print("Moving from ("); Serial.print(current_x); Serial.print(", "); Serial.print(current_y);
  Serial.print(") to ("); Serial.print(x); Serial.print(", "); Serial.print(y); Serial.println(")");

  move_double(x - current_x, y - current_y, half_period);
  current_x = x;
  current_y = y;
  
  Serial.println("Finished move");
  
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


/*
 * function move_double(int steps_x, int steps_y, int half_step_delay)
 * 
 * This function runs both motors the specified number of steps before returning to the caller.
 * It essentially blocks the rest of the program from execution until it has finished.
 * 
 * steps_x: the number of steps to move the X axis. Sign determines direction
 * steps_y: the number of steps to move the Y axis. Sign determines direction
 * half_step_delay: the delay (in microseconds) between each high and low write, equalling half the period of a pulse
 * 
 * Return: None
 */
void move_double(int steps_x, int steps_y, int half_step_delay) {

  if (steps_x == 0 && steps_y == 0) {
    Serial.println("Both step amounts are 0. Shortcutting out of here");
    return;
  }

  // UURRGHH not sure whether to refer to crossbeam axis as Y or Z.....

  // need to figure out which axis is moving more
  // in order to make general statements in the loop
  int more_steps, more_steps_pin, more_dir, more_dir_pin;
  int less_steps, less_steps_pin, less_dir, less_dir_pin;

  // the number of steps is being doubled because when we increment the counter
  // we'll be counting half-steps. So we need to count twice as many.
  
  if (abs(steps_x) > abs(steps_y)) {
    // we're moving further in the x direction than the y
    more_steps = abs(steps_x) * 2;
    more_steps_pin = X_STEP_PIN;
    more_dir = dir(steps_x);
    more_dir_pin = X_DIR_PIN;
    less_steps = abs(steps_y) * 2;
    less_steps_pin = Z_STEP_PIN;
    less_dir = dir(steps_y);
    less_dir_pin = Z_DIR_PIN;
  }
  else {
    // we're moving further in the y direction than the x
    more_steps = abs(steps_y) * 2;
    more_steps_pin = Z_STEP_PIN;
    more_dir = dir(steps_y);
    more_dir_pin = Z_DIR_PIN;
    less_steps = abs(steps_x) * 2;
    less_steps_pin = X_STEP_PIN;
    less_dir = dir(steps_x);
    less_dir_pin = X_DIR_PIN;
  }

  if (less_steps == 0) {
    Serial.println("One of the step directions was 0. Shortcutting out of here");
    move_blocking(more_steps_pin, more_dir_pin, more_steps / 2, more_dir, half_step_delay);
    return;
  }

  // set direction
  digitalWrite(more_dir_pin, more_dir);
  digitalWrite(less_dir_pin, less_dir);

  // set delay: traveling shorter distance -> longer duration of pulses
  int other_step_delay = abs((float)half_step_delay * more_steps / less_steps);

  // debugging feedback
  Serial.print("More axis:    "); Serial.println(more_steps_pin);
  Serial.print("  half steps: "); Serial.println(more_steps);
  Serial.print("       delay: "); Serial.println(half_step_delay);
  Serial.print("   direction: "); Serial.println(more_dir);
  Serial.print("     dir pin: "); Serial.println(more_dir_pin);
  Serial.println();
  Serial.print("Less axis:    "); Serial.println(less_steps_pin);
  Serial.print("  half steps: "); Serial.println(less_steps);
  Serial.print("       delay: "); Serial.println(other_step_delay);
  Serial.print("   direction: "); Serial.println(less_dir);
  Serial.print("     dir pin: "); Serial.println(less_dir_pin);
    
  // half-step counters
  int more_counter = 0;
  int less_counter = 0;

  // HIGH or LOW pulse trackers
  int more_pulse = HIGH;
  int less_pulse = HIGH;

  // timestamp for remembering last time we send a pulse to a motor
  int more_previous = micros();
  int less_previous = more_previous;

  // do movement
  while (more_counter < more_steps && less_counter < less_steps) {

    long current_time = micros();

    if (current_time - more_previous > half_step_delay) {
      digitalWrite(more_steps_pin, more_pulse);
      more_pulse = (more_pulse + 1) % 2;
      more_previous = current_time;
      more_counter++;
    }

    if (current_time - less_previous > other_step_delay) {
      digitalWrite(less_steps_pin, less_pulse);
      less_pulse = (less_pulse + 1) % 2;
      less_previous = current_time;
      less_counter++;
    }
  }

//  Serial.println("Finished simultaneous motor movement");
}
