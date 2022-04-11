


const int X_STOP_NEG = 9;  // labeled as "Limit X-axis"
const int X_STOP_POS = 10; // labeled as "Limit Y-axis"
const int Z_STOP_NEG = 11; // labeled as "Limit Z-axis"
const int Z_STOP_POS = 6;  // labeled as "Y DIR"


const int X_STEP_PIN = 2;
const int X_DIR_PIN = 5;
const int Z_STEP_PIN = 4;
const int Z_DIR_PIN = 7;

//int LAST_X_DIR = LOW;
//int LAST_Z_DIR = LOW;

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

//const int RANGES[] =              {10,  200,  400, 480, 999};
//const int STEPS[] =               { 0,    3,    5,   8,  10};
//const unsigned long DURATIONS[] = { 0, 2000, 1200, 750, 500};
//const int ARRAY_SIZE = 5;

const int RANGES[] =              {10,  380, 450, 999};
const int STEPS[] =               { 0,    5,   8,  10};
const unsigned long DURATIONS[] = { 0, 1200, 750, 600};
const int ARRAY_SIZE = 4;


#define dir(x) ((x) < 0 ? LOW : HIGH)

void setup() {

  pinMode(X_STEP_PIN, OUTPUT);
  pinMode(X_DIR_PIN, OUTPUT);
  pinMode(Z_STEP_PIN, OUTPUT);
  pinMode(Z_DIR_PIN, OUTPUT);

  // use the builtin pullup resistors
  // when the switch is activated, these pins will read LOW
  // this is called active low, I think
  pinMode(X_STOP_NEG, INPUT_PULLUP);
  pinMode(X_STOP_POS, INPUT_PULLUP);
  pinMode(Z_STOP_NEG, INPUT_PULLUP);
  pinMode(Z_STOP_POS, INPUT_PULLUP);

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

      if (digitalRead(X_STOP_NEG) == LOW && x_dir == LOW) {
        Serial.print("Cannot move in -X direction: "); Serial.println(x_counter);
        x_counter = x_steps;
        
      } else if (digitalRead(X_STOP_POS) == LOW && x_dir == HIGH) {
        Serial.print("Cannot move in +X direction: "); Serial.println(x_counter);
        x_counter = x_steps;
        
      } else {
//        Serial.print("x pulse"); Serial.print(x_pulse); Serial.print(" at "); Serial.println(current_time);
        digitalWrite(X_STEP_PIN, x_pulse);
        x_pulse = (x_pulse + 1) % 2;
        x_previous = current_time;
        x_counter++;
//        LAST_X_DIR = x_dir;
      }

    }

    if (current_time - y_previous > y_period && y_counter < y_steps) {

      if (digitalRead(Z_STOP_NEG) == LOW && y_dir == LOW) {
        // no movement, could add print statement
        Serial.println("Cannot move in -Z direction");
        y_counter = y_steps;
        
      } else if (digitalRead(Z_STOP_POS) == LOW && y_dir == HIGH) {
        // no movement, could add print statement
        Serial.println("Cannot move in +Z direction");
        y_counter = y_steps;
        
      } else {
//        Serial.print("y pulse "); Serial.println(y_pulse);
        digitalWrite(Z_STEP_PIN, y_pulse);
        y_pulse = (y_pulse + 1) % 2;
        y_previous = current_time;
        y_counter++;
//        LAST_Z_DIR = y_dir;
      }
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
