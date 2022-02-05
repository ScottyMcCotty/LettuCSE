


//const int MAX_SPEED = 300;
//const int START_SPEED = 20;
//const double PROPORTION = 0.2;
//const double p_i = 300000.0 / START_SPEED;
//const double p_f = 300000.0 / MAX_SPEED;

const int STEPS_TO_MAX_SPEED = 300;

const int STEP_PIN = 4;
const int DIR_PIN = 7;

double coefficient = 0.0;

//const int delays[] = {3700, 3700, 3700,
//                      3400, 3400, 3400,
//                      3100, 3100, 3100,
//                      2800, 2800, 2800,
//                      2500, 2500, 2500,
//                      2200, 2200, 2200,
//                      1900, 1900, 1900,
//                      1600, 1600, 1600,
//                      1300, 1300, 1300,
//                      1000, 1000, 1000,
//                      900, 900, 900,
//                      800, 800, 800,
//                      700, 700, 700,
//                      600, 600, 600};

int delays[STEPS_TO_MAX_SPEED] = {1000};


void setup() {

  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  
  Serial.begin(9600);


  delay(500);
  populate_delay_array();


//  coefficient = (p_i - p_f) / (p_f * PROPORTION * num_steps);

//  Serial.println("Parameters:");
//  Serial.print("  T: "); Serial.println(num_steps);
//  Serial.print("  A: "); Serial.println(PROPORTION);
//  Serial.print("  S: "); Serial.println(START_SPEED);
//  Serial.print("  F: "); Serial.println(MAX_SPEED);
//  Serial.print("  m: "); Serial.println(coefficient);

//  int delay_time;
//  int steps = 0;
//  digitalWrite(DIR_PIN, LOW);
//  while (steps < num_steps) {
//    if (steps < PROPORTION * num_steps) {
//      delay_time = p_i / (coefficient * steps + 1);
//    }
//    else if (steps > (1 - PROPORTION) * num_steps) {
//      delay_time = p_i / (coefficient * (num_steps - steps) + 1);
//    }
//    else {
//      delay_time = 300000 / MAX_SPEED;
//    }
//
//    int vel = 300000 / delay_time;
//    Serial.println(delay_time / 2);
//    Serial.println(vel);

//    move_single_step(delay_time / 2);
//    move_single_step(delays[8]);
//    Serial.println("slow 'er down");
//    
//    steps++;
//  }

  
}

void loop() {
  // put your main code here, to run repeatedly:
  move_there_and_back();
}


void move_there_and_back() {
  
  String input = wait_for_input();

  int num_steps = input.toInt();
  
  smooth_velocity(STEP_PIN, DIR_PIN, num_steps, HIGH);

  reset_motor(num_steps);
}


void populate_delay_array() {

  const double START = 2000.0; // delay at lowest (starting) speed
  const double TARGET = 300.0; // delay at highest (target) speed
  const int STEPS = STEPS_TO_MAX_SPEED; // number of steps to reach top speed

  const double m = (1.0 - (TARGET / START)) / (TARGET * STEPS);
  const double b = 1.0 / START;

  for (int ii = 0; ii < STEPS; ++ii) {
    double p = 1.0 / (m * ii + b);
    delays[ii] = int(p);
    Serial.print("delay "); Serial.print(ii); Serial.print(": ");
    Serial.println(delays[ii]);
  }
  
}


void smooth_velocity(int motor_step_pin, int motor_direction_pin, int num_steps, int dir) {

//  Serial.print("Moving single axis "); Serial.println(motor_step_pin);
//  Serial.print("  steps = "); Serial.println(num_steps);
//  Serial.print("  direction = "); Serial.println(dir);
//  Serial.print("  dir pin = "); Serial.println(motor_direction_pin);

  // double the number of steps because we're incrementing every half-step!!
  // actually, don't do this because we're only going to count low pulses as steps
//  num_steps = num_steps * 2;

  // set direction
  digitalWrite(motor_direction_pin, dir);

  // set up for movement
  int counter = 0;
  unsigned long othercounter = 0;
  int pulse = HIGH;
  unsigned long previous = micros();

  int delay_time = delays[0];

  while (counter < num_steps) {

    unsigned long current = micros();
    
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

  Serial.println("Finished move:");
  Serial.print("  # times skipped: "); Serial.println(othercounter);
  Serial.print("  # times pulsed:  "); Serial.println(num_steps);
  
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


void reset_motor(int num_steps) {

  delay(2000);
  digitalWrite(DIR_PIN, LOW);
  for (int ii = 0; ii < num_steps; ++ii) {
    move_single_step(1200);
  }

}

void move_single_step(int dt) {
  digitalWrite(STEP_PIN, HIGH);
  delayMicroseconds(dt);
  digitalWrite(STEP_PIN, LOW);
  delayMicroseconds(dt);
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

  Serial.println("Waiting to go, send number of steps");
  
  while (state == 0) {
//    Serial.print("Waiting to start... send any key ("); Serial.print(++count); Serial.println(")");
    state = Serial.readBytesUntil('\n', buf, 10);
  }

//  Serial.print("Received input: '"); Serial.print(buf); Serial.println("'");

  return String(buf);
}
