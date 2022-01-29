
// Stepper Motor X
const int X_STEP_PIN = 2;
const int X_DIR_PIN = 5;
//const int Y_STEP_PIN = 3;
//const int Y_DIR_PIN = 6;
const int Z_STEP_PIN = 4;
const int Z_DIR_PIN = 7;

#define dir(x) ((x) < 0 ? LOW : HIGH)

void setup() {
  // Sets the two pins as Outputs
  pinMode(X_STEP_PIN, OUTPUT); 
  pinMode(X_DIR_PIN, OUTPUT);
  pinMode(Z_STEP_PIN, OUTPUT); 
  pinMode(Z_DIR_PIN, OUTPUT);
  
  Serial.begin(9600);
  Serial.setTimeout(2000);

  // block here until the user sends something
  wait_for_input("start");

  Serial.println("Setup finished");

  move_double(-400, -400, 700);
  delay(1000);
  move_double(400, 400, 700);
}

void loop() {

  String input = wait_for_input("move");
  
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
    Serial.print("Waiting to " + prompt + " ("); Serial.print(++count); Serial.println(")");
    state = Serial.readBytesUntil('\n', buf, 10);
  }

  Serial.print("Received input: '"); Serial.print(buf); Serial.println("'");

  return String(buf);
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

  // set direction
  digitalWrite(more_dir_pin, more_dir);
  digitalWrite(less_dir_pin, less_dir);

  // set delay: traveling shorter distance -> longer duration of pulses
  long other_step_delay = half_step_delay * abs(more_steps) / abs(less_steps);

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
    }

    if (current_time - less_previous > other_step_delay) {
      digitalWrite(less_steps_pin, less_pulse);
      less_pulse = (less_pulse + 1) % 2;
      less_previous = current_time;
    }
  }

  Serial.println("Finished simultaneous motor movement");
}
