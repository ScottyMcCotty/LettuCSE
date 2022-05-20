

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

const double TARGET = 250.0; // delay at highest (target) speed
const double START = 900.0;  // delay at starting speed
const int STEPS_TO_MAX_SPEED = 400;
int delays[STEPS_TO_MAX_SPEED] = {1100};

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

  populate_delay_array();

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
    Serial.println("Calibrated");

  }
  else {

//    Serial.println("I'm moving");
    int space = input.indexOf(" ");
    int x = input.substring(0, space).toInt();
    int y = input.substring(space+1).toInt();
  
//     Serial.print("Split into '"); Serial.print(x); Serial.print("' and '"); Serial.print(y); Serial.println("'");
  
    move_coordinates(x, y);
  }  
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

  int steps_x = x - current_x;
  // move_blocking(X_STEP_PIN, X_DIR_PIN, abs(steps_x), dir(steps_x), half_period, X_STOP_PIN);
  smooth_velocity(X_STEP_PIN, X_DIR_PIN, abs(steps_x), dir(steps_x), X_STOP_PIN);
  
  int steps_y = y - current_y;
  // move_blocking(Z_STEP_PIN, Z_DIR_PIN, abs(steps_y), dir(steps_y), half_period, Z_STOP_PIN);
  smooth_velocity(Z_STEP_PIN, Z_DIR_PIN, abs(steps_y), dir(steps_y), Z_STOP_PIN);


  current_x = x;
  current_y = y;
  
  Serial.println("Done");
  
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
 * stop_pin: the pin to check whether the limit switch has been hit
 * 
 * Return: None
 */
void move_blocking(int motor_step_pin, int motor_direction_pin, int num_steps, int dir, int half_step_delay, int stop_pin) {
  
  //  Serial.print("Moving single axis "); Serial.println(motor_step_pin);
  //  Serial.print("  steps = "); Serial.println(num_steps);
  //  Serial.print("  direction = "); Serial.println(dir);
  //  Serial.print("  dir pin = "); Serial.println(motor_direction_pin);
  //  Serial.print("  delay = "); Serial.println(half_step_delay);
  //  Serial.print("  stop pin = "); Serial.println(stop_pin);

  bool limit_triggered = false;

  // set direction
  digitalWrite(motor_direction_pin, dir);

  // do movement
  for (int ii = 0; ii < num_steps; ii++) {

    
    if (digitalRead(stop_pin) == LOW) {
      limit_triggered = true;
      break;
    }

    digitalWrite(motor_step_pin, HIGH);
    delayMicroseconds(half_step_delay);
    digitalWrite(motor_step_pin, LOW);
    delayMicroseconds(half_step_delay);
  }

  if (limit_triggered) {
    Serial.println("Blocking movement ended early because limit switch was triggered");
  }
}


void populate_delay_array() {

  const double m = (1.0 - (TARGET / START)) / (TARGET * STEPS_TO_MAX_SPEED);
  const double b = 1.0 / START;

  for (int ii = 0; ii < STEPS_TO_MAX_SPEED; ++ii) {
    double p = 1.0 / (m * ii + b);
    delays[ii] = int(p);
    // Serial.print("delay "); Serial.print(ii); Serial.print(": ");
    // Serial.println(delays[ii]);
  }
  
}

void smooth_velocity(int motor_step_pin, int motor_direction_pin, int num_steps, int dir, int stop_pin) {

//  Serial.print("Moving pin = "); Serial.print(motor_step_pin); Serial.print(", steps = "); Serial.println(num_steps);

  if (num_steps < STEPS_TO_MAX_SPEED * 2) {
    move_blocking(motor_step_pin, motor_direction_pin, num_steps, dir, half_period, stop_pin);
    return;
  }

//  Serial.println("SMOOTH VELOCITY:");
//  Serial.print("Moving single axis "); Serial.println(motor_step_pin);
//  Serial.print("  steps = "); Serial.println(num_steps);
//  Serial.print("  direction = "); Serial.println(dir);
//  Serial.print("  dir pin = "); Serial.println(motor_direction_pin);
//  Serial.print("  stop pin = "); Serial.println(stop_pin);
    
  // set direction
  digitalWrite(motor_direction_pin, dir);

  // set up for movement
  int counter = 0;
  unsigned long othercounter = 0;
  int pulse = HIGH;
  unsigned long previous = micros();
//  bool limit_triggered = false;

  int delay_time = delays[0];

  while (counter < num_steps) {

    unsigned long current = micros();
    
//    if (digitalRead(stop_pin) == LOW) {
//      limit_triggered = true;
//      break;
//    }
    
    if (current - previous > delay_time) {
      digitalWrite(motor_step_pin, pulse);
      if (pulse == HIGH) {
        // after sending a high pulse, recalculate the delay time
        delay_time = calculate_new_delay(counter, num_steps);
      }
      else {
        // after sending a low pulse, increment the counter
        counter++;
      }
      pulse = (pulse + 1) % 2;
      previous = current;
//      counter++;
    }
    else {
      othercounter++;
    }
  }

//  Serial.print("After velocity movement: counter = "); Serial.print(counter);
//  Serial.print(", othercounter = "); Serial.println(othercounter);
//  if (limit_triggered) {
//    Serial.println("Movement ended because limit switch was triggered");
//  }
}
  
int calculate_new_delay(int n, int steps) {
  if (n < STEPS_TO_MAX_SPEED) {
    return delays[n];
  }
  if ((steps - n) < STEPS_TO_MAX_SPEED) {
    return delays[steps-n];
  }
  return delays[STEPS_TO_MAX_SPEED - 1];
}
