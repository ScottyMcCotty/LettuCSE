// Stepper Motor X
const int X_STEP_PIN = 2;
const int X_DIR_PIN = 5;
//const int Y_STEP_PIN = 4;
//const int Y_DIR_PIN = 6;
const int Z_STEP_PIN = 4;
const int Z_DIR_PIN = 7;

const int PULSE_DUR = 500; // Duration of step pulses
const int NUM_STEPS = 800; // Number of steps (only used for some loops)
 
void setup() {
  // Sets the two pins as Outputs
  pinMode(X_STEP_PIN, OUTPUT); 
  pinMode(X_DIR_PIN, OUTPUT);
  pinMode(Z_STEP_PIN, OUTPUT); 
  pinMode(Z_DIR_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  /*
  // Set direction to "positive"/high for both directions
  Serial.println("pos/high direction");
  digitalWrite(X_DIR_PIN, HIGH);
  digitalWrite(Z_DIR_PIN, HIGH);

  for(int x = 0; x < NUM_STEPS; x++) {
    //digitalWrite(X_STEP_PIN, HIGH); // uncomment to also move X motors
    digitalWrite(Z_STEP_PIN, HIGH);
    delayMicroseconds(PULSE_DUR);
    //digitalWrite(X_STEP_PIN, LOW);
    digitalWrite(Z_STEP_PIN, LOW);
    delayMicroseconds(PULSE_DUR);
  }
  delay(2000); // Two second delay

  // Set direction to "negative"/low for both directions
  Serial.println("neg/low direction");
  digitalWrite(X_DIR_PIN, LOW);
  digitalWrite(Z_DIR_PIN, LOW);

  for(int x = 0; x < NUM_STEPS; x++) {
    //digitalWrite(X_STEP_PIN, HIGH);
    digitalWrite(Z_STEP_PIN, HIGH);
    delayMicroseconds(PULSE_DUR);
    //digitalWrite(X_STEP_PIN, LOW);
    digitalWrite(Z_STEP_PIN, LOW);
    delayMicroseconds(PULSE_DUR);
  }
  delay(2000); // Two second delay
  */

  // Attempt to move silkscreen-specified Z motor all the way across crossbeam
  digitalWrite(Z_DIR_PIN, LOW);
  for(int x = 0; x < 5600; x++) {
    digitalWrite(Z_STEP_PIN, HIGH);
    delayMicroseconds(PULSE_DUR);
    digitalWrite(Z_STEP_PIN, LOW);
    delayMicroseconds(PULSE_DUR);
  }
  // and back
  digitalWrite(Z_DIR_PIN, HIGH);
  for(int x = 0; x < 5600; x++) {
    digitalWrite(Z_STEP_PIN, HIGH);
    delayMicroseconds(PULSE_DUR);
    digitalWrite(Z_STEP_PIN, LOW);
    delayMicroseconds(PULSE_DUR);
  }
}
