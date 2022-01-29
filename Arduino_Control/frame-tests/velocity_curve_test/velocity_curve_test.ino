


const int MAX_SPEED = 50;
const int START_SPEED = 20;
const double PROPORTION = 0.2;
const double p_i = 300000.0 / START_SPEED;
const double p_f = 300000.0 / MAX_SPEED;

double coefficient = 0.0;

void setup() {

  Serial.begin(9600);

  String input = wait_for_input();

  int num_steps = input.toInt();

  coefficient = (p_i - p_f) / (p_f * PROPORTION * num_steps);

//  Serial.println("Parameters:");
//  Serial.print("  T: "); Serial.println(num_steps);
//  Serial.print("  A: "); Serial.println(PROPORTION);
//  Serial.print("  S: "); Serial.println(START_SPEED);
//  Serial.print("  F: "); Serial.println(MAX_SPEED);
//  Serial.print("  m: "); Serial.println(coefficient);

  int delay_time;
  
  int steps = 0;

  while (steps < num_steps) {
    if (steps < PROPORTION * num_steps) {
      delay_time = p_i / (coefficient * steps + 1);
    }
    else if (steps > (1 - PROPORTION) * num_steps) {
      delay_time = p_i / (coefficient * (num_steps - steps) + 1);
    }
    else {
      delay_time = 300000 / MAX_SPEED;
    }

    int vel = 300000 / delay_time;
    Serial.println(vel);
    steps++;
  }
  
}

void loop() {
  // put your main code here, to run repeatedly:

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
//    Serial.print("Waiting to start... send any key ("); Serial.print(++count); Serial.println(")");
    state = Serial.readBytesUntil('\n', buf, 10);
  }

//  Serial.print("Received input: '"); Serial.print(buf); Serial.println("'");

  return String(buf);
}
