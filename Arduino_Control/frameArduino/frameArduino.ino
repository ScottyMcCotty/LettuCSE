


const int X_STOP_PIN = 9; // this won't compile until an actual pin is selected
const int Z_STOP_PIN = 11; // not sure what pin it will be yet


const int X_STEP_PIN = 2;
const int X_DIR_PIN = 5;
const int Z_STEP_PIN = 4;
const int Z_DIR_PIN = 7;

int current_x = 0;
int current_y = 0;

const int half_period = 1100;
const String CALIBRATION_STRING = "calibrate";

//String buf = "";
bool string_complete = false;

#define dir(x) ((x) < 0 ? LOW : HIGH)

void setup() {

  pinMode(X_STEP_PIN, OUTPUT);
  pinMode(X_DIR_PIN, OUTPUT);
  pinMode(Z_STEP_PIN, OUTPUT);
  pinMode(Z_DIR_PIN, OUTPUT);

  // use the builtin pullup resistors
  // when the switch is activated, these pins will read LOW
  // this is called active low, I think
  pinMode(X_STOP_PIN, INPUT_PULLUP);
  pinMode(Z_STOP_PIN, INPUT_PULLUP);

  Serial.begin(9600);
//  Serial.begin(115200);

  delay(500); // feels right

  Serial.println("Hello, world!");

}

void loop() {
  
  String input = wait_for_input("Absolute move coordinates? ");

//  Serial.println("this is the frame. I received: " + input);
  
  if (input == CALIBRATION_STRING) {

//    Serial.println("I'm calibrating");
    auto_calibrate_axis(X_STEP_PIN, X_DIR_PIN, X_STOP_PIN);
    auto_calibrate_axis(Z_STEP_PIN, Z_DIR_PIN, Z_STOP_PIN);

    current_x = 0;
    current_y = 0;
  }
  else {

//    Serial.println("I'm moving");
    int space = input.indexOf(" ");
    int x = input.substring(0, space).toInt();
    int y = input.substring(space+1).toInt();
  
    Serial.print("Split into '"); Serial.print(x); Serial.print("' and '"); Serial.print(y); Serial.println("'");
  
    move_coordinates(x, y);
  }

  Serial.println("Done");
  
}


void auto_calibrate_axis(int motor_pin, int dir_pin, int stop_pin) {
//  Serial.print("Auto-calibrating pin "); Serial.println(motor_pin);
  // Serial.println("Enter integer, or 'save'");

  // set direction negative
  digitalWrite(dir_pin, LOW);
  while (digitalRead(stop_pin) == HIGH) {
    // motor hasn't been triggered yet, keep rolling in negative direction
    digitalWrite(motor_pin, HIGH);
    delayMicroseconds(half_period);
    digitalWrite(motor_pin, LOW);
    delayMicroseconds(half_period);
//    Serial.println("Moving negative");
//    delay(200);
  }

  delay(500);

  // we ran into the limit switch, now we want to back off a bit until it's not being touched
  digitalWrite(dir_pin, HIGH);
  while(digitalRead(stop_pin) == LOW) {
    // move it slowly away from the limit switch
    digitalWrite(motor_pin, HIGH);
    delayMicroseconds(half_period * 2);
    digitalWrite(motor_pin, LOW);
    delayMicroseconds(half_period * 2);
  }

  Serial.println("Calibrated");
  // we can say this is the home position. Barely just in front of triggering the limit switch
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

  char buf[] = {'\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0',
                '\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0'};

//  Serial.println("\n" + prompt);
  
  while (state == 0) {
//    Serial.print(prompt); Serial.println(++count);
    state = Serial.readBytesUntil('\n', buf, 20);
//    while (Serial.available()) {
//      Serial.read();
//    }
  }
//  Serial.print("Received input: '"); Serial.print(buf); Serial.println("'");
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

  // if (current_x == -1 || current_y == -1) {
  //   return;
  // }

//  Serial.print("Moving from ("); Serial.print(current_x); Serial.print(", "); Serial.print(current_y);
//  Serial.print(") to ("); Serial.print(x); Serial.print(", "); Serial.print(y); Serial.println(")");

  // for moving diagonally:
  // move_double(x - current_x, y - current_y, half_period);

  int steps_x = x - current_x;
  move_blocking(X_STEP_PIN, X_DIR_PIN, abs(steps_x), dir(steps_x), half_period, X_STOP_PIN)
  int steps_y = y - current_y;
  move_blocking(Z_STEP_PIN, Y_DIR_PIN, abs(steps_y), dir(steps_y), half_period, Z_STOP_PIN)


  current_x = x;
  current_y = y;
  
//  Serial.println("Finished move");
  
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
void move_blocking(int motor_step_pin, int motor_direction_pin, int num_steps, int dir, int half_step_delay, int stop_pin) {
  
  // set direction
  digitalWrite(motor_direction_pin, dir);

  // do movement
  for (int ii = 0; ii < num_steps; ii++) {

    if (digitalRead(stop_pin) == HIGH) {
      break;
    }
    
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
//    Serial.println("Both step amounts are 0. Shortcutting out of here");
    return;
  }

  // UURRGHH not sure whether to refer to crossbeam axis as Y or Z.....

  // need to figure out which axis is moving more
  // in order to make general statements in the loop
  int more_steps, more_steps_pin, more_dir, more_dir_pin, more_stop_pin;
  int less_steps, less_steps_pin, less_dir, less_dir_pin, less_stop_pin;

  // the number of steps is being doubled because when we increment the counter
  // we'll be counting half-steps. So we need to count twice as many.
  
  if (abs(steps_x) > abs(steps_y)) {
    // we're moving further in the x direction than the y
    more_steps = abs(steps_x) * 2;
    more_steps_pin = X_STEP_PIN;
    more_dir = dir(steps_x);
    more_dir_pin = X_DIR_PIN;
    more_stop_pin = X_STOP_PIN;
    less_steps = abs(steps_y) * 2;
    less_steps_pin = Z_STEP_PIN;
    less_dir = dir(steps_y);
    less_dir_pin = Z_DIR_PIN;
    less_stop_pin = Z_STOP_PIN;
  }
  else {
    // we're moving further in the y direction than the x
    more_steps = abs(steps_y) * 2;
    more_steps_pin = Z_STEP_PIN;
    more_dir = dir(steps_y);
    more_dir_pin = Z_DIR_PIN;
    more_stop_pin = Z_STOP_PIN;
    less_steps = abs(steps_x) * 2;
    less_steps_pin = X_STEP_PIN;
    less_dir = dir(steps_x);
    less_dir_pin = X_DIR_PIN;
    less_stop_pin = X_STOP_PIN;
  }

  if (less_steps == 0) {
//    Serial.println("One of the step directions was 0. Shortcutting out of here");
    move_blocking(more_steps_pin, more_dir_pin, more_steps / 2, more_dir, half_step_delay, more_stop_pin);
    return;
  }

  // just call move_blocking twice to achieve the same movement but slower
//  move_blocking(more_steps_pin, more_dir_pin, more_steps / 2, more_dir, half_step_delay);
//  move_blocking(less_steps_pin, less_dir_pin, less_steps / 2, less_dir, half_step_delay);
//  return;
  

  // set direction
  digitalWrite(more_dir_pin, more_dir);
  digitalWrite(less_dir_pin, less_dir);

  // set delay: traveling shorter distance -> longer duration of pulses
  int other_step_delay = abs((float)half_step_delay * more_steps / less_steps);

  // debugging feedback
//  Serial.print("More axis:    "); Serial.println(more_steps_pin);
//  Serial.print("  half steps: "); Serial.println(more_steps);
//  Serial.print("       delay: "); Serial.println(half_step_delay);
//  Serial.print("   direction: "); Serial.println(more_dir);
//  Serial.print("     dir pin: "); Serial.println(more_dir_pin);
//  Serial.println();
//  Serial.print("Less axis:    "); Serial.println(less_steps_pin);
//  Serial.print("  half steps: "); Serial.println(less_steps);
//  Serial.print("       delay: "); Serial.println(other_step_delay);
//  Serial.print("   direction: "); Serial.println(less_dir);
//  Serial.print("     dir pin: "); Serial.println(less_dir_pin);
    
  // half-step counters
  int more_counter = 0;
  int less_counter = 0;

  // HIGH or LOW pulse trackers
  int more_pulse = HIGH;
  int less_pulse = HIGH;

  // timestamp for remembering last time we send a pulse to a motor
  unsigned long more_previous = micros();
  unsigned long less_previous = more_previous;

  // do movement
  while (more_counter < more_steps && less_counter < less_steps) {

    unsigned long current_time = micros();

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
