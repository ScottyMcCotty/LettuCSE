//
// Allows manual control of the forklift toolhead via two buttons:
// - up button: connects analog pin 0 (reset/abort) to ground to lift fork
// - down button: connects analog pin 1 (feed hold) to ground to lower fork
//
// Assumes that the lifting motor is installed as the X axis motor with the
// following axis limits:
// - X axis limit: fork has been lowered to maximum
// - Y axis limit: fork has been lowered to tray
// - Z axis limit: forklift has been raised to maximum
//


//
// Constants
//

// Button pins
const int BUTTON_UP = A0;
const int BUTTON_DOWN = A1;

// X axis motor control pins
const int STEP_PIN = 2;
const int DIR_PIN = 5;

const int LIMIT_LOWER_MAX_PIN = 9; // X axis limit
const int LIMIT_TRAY_PIN = 10;     // Y axis limit
const int LIMIT_LIFT_MAX_PIN = 11; // Z axis limit

const int HALF_PERIOD = 700; // microseconds
const int QUARTER_PERIOD = HALF_PERIOD / 2;


//
// Global variables
//

//bool debug = true; // Set to false to disable debugging output
bool debug = false;


//
// Main procedures
//

void setup() {
  if (debug) set_up_serial();
  set_up_pins();
}


void loop() {
  if (up_button_pressed()) {
    if (debug) Serial.println("Up button pressed");
    send_up_pulse();
  } else if (down_button_pressed()) {
    if (debug) Serial.println("Down button pressed");
    send_down_pulse();
  }
}


//
// Helper functions
//

void set_up_serial() {
  Serial.begin(115200);
  delay(500);
  Serial.println("Serial setup complete, debugging messages enabled");
}


void set_up_pins() {
  pinMode(BUTTON_UP, INPUT_PULLUP);
  pinMode(BUTTON_DOWN, INPUT_PULLUP);
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(LIMIT_LOWER_MAX_PIN, INPUT_PULLUP);
  pinMode(LIMIT_TRAY_PIN, INPUT_PULLUP);
  pinMode(LIMIT_LIFT_MAX_PIN, INPUT_PULLUP);

  if (debug) print_pin_setup();
}


void print_pin_setup() {
  Serial.println("====== PIN SETUP ======");
  Serial.println("Up button:");
  Serial.println(BUTTON_UP);
  Serial.println("Down button:");
  Serial.println(BUTTON_DOWN);
  Serial.println("Step pin:");
  Serial.println(STEP_PIN);
  Serial.println("Directioin pin:");
  Serial.println(DIR_PIN);
  Serial.println("Lower limit switch pin:");
  Serial.println(LIMIT_LOWER_MAX_PIN);
  Serial.println("Tray limit switch pin:");
  Serial.println(LIMIT_TRAY_PIN);
  Serial.println("Upper limit switch pin");
  Serial.println(LIMIT_LIFT_MAX_PIN);
  Serial.println("\n");
}


// TODO: differentiate these with limit switch logic
void send_up_pulse() {
  digitalWrite(DIR_PIN, LOW);
  digitalWrite(STEP_PIN, LOW);
  delayMicroseconds(QUARTER_PERIOD);
  digitalWrite(STEP_PIN, HIGH);
  delayMicroseconds(HALF_PERIOD);
  digitalWrite(STEP_PIN, LOW);
  delayMicroseconds(QUARTER_PERIOD);
}


void send_down_pulse() {
  digitalWrite(DIR_PIN, HIGH);
  digitalWrite(STEP_PIN, LOW);
  delayMicroseconds(QUARTER_PERIOD);
  digitalWrite(STEP_PIN, HIGH);
  delayMicroseconds(HALF_PERIOD);
  digitalWrite(STEP_PIN, LOW);
  delayMicroseconds(QUARTER_PERIOD);
}


bool up_button_pressed() {
  return digitalRead(BUTTON_UP) == LOW;
}


bool down_button_pressed() {
  return digitalRead(BUTTON_DOWN) == LOW;
}
