


const int X_STOP_PIN = 9; // this won't compile until an actual pin is selected
const int Z_STOP_PIN = 11; // not sure what pin it will be yet


const int X_STEP_PIN = 2;
const int X_DIR_PIN = 5;
const int Z_STEP_PIN = 4;
const int Z_DIR_PIN = 7;

const int VRx = A0;
const int VRy = A1;
//const int SW = ;
const int CALIBRATION_SIZE = 100;
int xBias;
int yBias;

//const int half_period = 1100;

const int MAX_NUM_STEPS = 10;
//const int MIN_PULSE_DURATION = 600;
//const int FULL_DURATION = NUM_JOYSTICK_STEPS * MIN_PULSE_DURATION * 2;
const int RANGES[] =              {10,  200,  400, 480, 999};
const int STEPS[] =               { 0,    3,    5,   8,  10};
const unsigned long DURATIONS[] = { 0, 2000, 1200, 750, 500};
const int ARRAY_SIZE = 5;

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

  pinMode(VRx, INPUT);
  pinMode(VRy, INPUT);
//  pinMode(SW, INPUT_PULLUP);

//  Serial.begin(9600);
  Serial.begin(115200);

  delay(500); // feels right
  
  calculateBias();

//  Serial.println("Hello, world!");
  
//  wait_for_input("Waiting to start (any keys)");

//  do_square(300);
  

  // calibration routine
//   calibrate_axis(X_STEP_PIN, X_DIR_PIN);
//   calibrate_axis(Z_STEP_PIN, Z_DIR_PIN);

  // auto calibration routine
//  auto_calibrate_axis(Z_STEP_PIN, Z_DIR_PIN, Z_STOP_PIN);

//  calibrate_axis(Z_STEP_PIN, Z_DIR_PIN);

//  current_x = 0;
//  current_y = 0;
//  Serial.println("Home has been set!\nAbsolute coordinate mode activated");

}

void loop() {

//  unsigned long then = micros();
  
  int ax = -1 * doScaling(analogRead(VRx), xBias);
  int ay = -1 * doScaling(analogRead(VRy), yBias);

//  unsigned long now = micros();
  
//  Serial.println(now - then);

  double_joystick_movement(ax, ay);

//  delay(200);

}

int doScaling(int value, int bias) {
  return value - bias;
  // this could be more complicated later?
}

int calculateIndex(int value) {
  value = abs(value);
//  Serial.print("value = "); Serial.println(value);
  for(int ii = 0; ii < ARRAY_SIZE; ++ii) {
    if (value < RANGES[ii]) {
      return ii;
    }
  }
  Serial.println("Somehow a value was outside the range of possible values");
}

//void auto_calibrate_axis(int motor_pin, int dir_pin, int stop_pin) {
////  Serial.print("Auto-calibrating pin "); Serial.println(motor_pin);
//  // Serial.println("Enter integer, or 'save'");
//
//  // set direction negative
//  digitalWrite(dir_pin, LOW);
//  while (digitalRead(stop_pin) == HIGH) {
//    // motor hasn't been triggered yet, keep rolling in negative direction
//    digitalWrite(motor_pin, HIGH);
//    delayMicroseconds(half_period);
//    digitalWrite(motor_pin, LOW);
//    delayMicroseconds(half_period);
////    Serial.println("Moving negative");
////    delay(200);
//  }
//
//  delay(500);
//
//  // we ran into the limit switch, now we want to back off a bit until it's not being touched
//  digitalWrite(dir_pin, HIGH);
//  while(digitalRead(stop_pin) == LOW) {
//    // move it slowly away from the limit switch
//    digitalWrite(motor_pin, HIGH);
//    delayMicroseconds(half_period * 2);
//    digitalWrite(motor_pin, LOW);
//    delayMicroseconds(half_period * 2);
//  }
//
//  Serial.println("Calibrated");
//  // we can say this is the home position. Barely just in front of triggering the limit switch
//}

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

//  string_complete = false;
//  buf = "";
//  while (!string_complete) {}
//
//  Serial.print("Received input: '"); Serial.print(buf); Serial.println("'");

//  return buf;
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
//void move_coordinates(int x, int y) {
//
//  if (current_x == -1 || current_y == -1) {
//    return;
//  }
//
////  Serial.print("Moving from ("); Serial.print(current_x); Serial.print(", "); Serial.print(current_y);
////  Serial.print(") to ("); Serial.print(x); Serial.print(", "); Serial.print(y); Serial.println(")");
//
//  move_double(x - current_x, y - current_y, half_period);
//  current_x = x;
//  current_y = y;
//  
////  Serial.println("Finished move");
//  
//}


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
//void move_blocking(int motor_step_pin, int motor_direction_pin, int num_steps, int dir, int half_step_delay) {
//
////  Serial.print("Moving single axis "); Serial.println(motor_step_pin);
////  Serial.print("  steps = "); Serial.println(num_steps);
////  Serial.print("  direction = "); Serial.println(dir);
////  Serial.print("  dir pin = "); Serial.println(motor_direction_pin);
////  Serial.print("  delay = "); Serial.println(half_step_delay);
//  
//  // set direction
//  digitalWrite(motor_direction_pin, dir);
//
//  // do movement
//  for (int ii = 0; ii < num_steps; ii++) {
//    digitalWrite(motor_step_pin, HIGH);
//    delayMicroseconds(half_step_delay);
//    digitalWrite(motor_step_pin, LOW);
//    delayMicroseconds(half_step_delay);
//  }
//
////  Serial.println("Finished move_blocking");
//}

void move_not_blocking(int motor_step_pin, int motor_direction_pin, int num_steps, int dir, int half_step_delay) {

//  Serial.print("Moving single axis "); Serial.println(motor_step_pin);
//  Serial.print("  steps = "); Serial.println(num_steps);
//  Serial.print("  direction = "); Serial.println(dir);
//  Serial.print("  dir pin = "); Serial.println(motor_direction_pin);
//  Serial.print("  delay = "); Serial.println(half_step_delay);

  // double the number of steps because we're incrementing every half-step!!
  num_steps = num_steps * 2;

  // set direction
  digitalWrite(motor_direction_pin, dir);

  // set up for movement
  int counter = 0;
  unsigned long othercounter = 0;
//  Serial.println(sizeof(othercounter));
  int pulse = HIGH;
  unsigned long previous = micros();

  while (counter < num_steps) {

    unsigned long current = micros();
    
    if (current - previous > half_step_delay) {
      digitalWrite(motor_step_pin, pulse);
      pulse = (pulse + 1) % 2;
      previous = current;
      counter++;
    }
    else {
      othercounter++;
    }
  }

//  Serial.println("Finished move:");
//  Serial.print("  # times skipped: "); Serial.println(othercounter);
//  Serial.print("  # times pulsed:  "); Serial.println(num_steps);
  
}


void double_joystick_movement(int ax, int ay) {
  
  int x_i = calculateIndex(ax);
  int y_i = calculateIndex(ay);

  unsigned long x_period = DURATIONS[x_i];
  unsigned long y_period = DURATIONS[y_i];
  int x_steps = STEPS[x_i];
  int y_steps = STEPS[y_i];
  int x_dir = dir(ax);
  int y_dir = dir(ay);

  if (x_steps == 0 && y_steps == 0) {
    Serial.println("No input, exiting early");
    return;
  }
//  if (x_steps == 0) {
//    Serial.println("No X, short-cutting");
//    move_not_blocking(Z_STEP_PIN, Z_DIR_PIN, y_steps, y_dir, y_period);
//    return;
//  }
//  if (y_steps == 0) {
//    Serial.println("No Y, short-cutting");
//    move_not_blocking(X_STEP_PIN, X_DIR_PIN, x_steps, x_dir, x_period);
//    return;
//  }

//  Serial.println(x_period);
//  Serial.println(y_period);
//  Serial.println(x_steps);
//  Serial.println(y_steps);
//  Serial.println(x_dir);
//  Serial.println(y_dir);
  
  digitalWrite(X_DIR_PIN, x_dir);
  digitalWrite(Z_DIR_PIN, y_dir);
  
  int x_counter = 0;
  int y_counter = 0;

  unsigned long x_previous = 0;
  unsigned long y_previous = 0;

  int x_pulse = HIGH;
  int y_pulse = HIGH;

  // do movement
  while (x_counter < x_steps || y_counter < y_steps) {

    unsigned long current_time = micros();

    if (current_time - x_previous > x_period && x_counter < x_steps) {
//      Serial.print("x pulse"); Serial.print(x_pulse); Serial.print(" at "); Serial.println(current_time);
      digitalWrite(X_STEP_PIN, x_pulse);
      x_pulse = (x_pulse + 1) % 2;
      x_previous = current_time;
      x_counter++;
    }

    if (current_time - y_previous > y_period && y_counter < y_steps) {
//      Serial.print("y pulse "); Serial.println(y_pulse);
      digitalWrite(Z_STEP_PIN, y_pulse);
      y_pulse = (y_pulse + 1) % 2;
      y_previous = current_time;
      y_counter++;
    }
  }

//  Serial.print("X moved: "); Serial.print(x_counter); Serial.print(" | X input: "); Serial.print(ax);
//  Serial.print(" | Y moved: "); Serial.print(y_counter); Serial.print(" | Y input: "); Serial.println(ay);
}

void calculateBias() {

  Serial.println("Calculating bias");

  double xValues = 0;
  double yValues = 0;
  
  for (int ii = 0; ii < CALIBRATION_SIZE; ++ii) {
    xValues += analogRead(VRx);
    yValues += analogRead(VRy);
  }

  int xAvg = round(xValues / (double)CALIBRATION_SIZE);
  int yAvg = round(yValues / (double)CALIBRATION_SIZE);

  xBias = xAvg;
  yBias = yAvg;

  Serial.print("X: total= "); Serial.print(xValues);
  Serial.print(" | avg= "); Serial.print(xAvg);
  Serial.print(" | bias= "); Serial.print(xBias);
  Serial.print(" | ("); Serial.print(CALIBRATION_SIZE); Serial.println(" values)");
  Serial.print("Y: total= "); Serial.print(yValues); 
  Serial.print(" | avg= "); Serial.print(yAvg);
  Serial.print(" | bias= "); Serial.print(yBias);
  Serial.print(" | ("); Serial.print(CALIBRATION_SIZE); Serial.println(" values)");
}
