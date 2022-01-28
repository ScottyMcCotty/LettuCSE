// Stepper Motor X
const int X_STEP_PIN = 2;
const int X_DIR_PIN = 5;
//const int Y_STEP_PIN = 4;
//const int Y_DIR_PIN = 6;
const int Z_STEP_PIN = 4;
const int Z_DIR_PIN = 7;

const int PULSE_DUR = 500;  // Duration of each pulse
const int NUM_STEPS = 8100; // Not used?
 
void setup() {
  // Sets the two pins as Outputs
  pinMode(X_STEP_PIN, OUTPUT); 
  pinMode(X_DIR_PIN, OUTPUT);
  pinMode(Z_STEP_PIN, OUTPUT); 
  pinMode(Z_DIR_PIN, OUTPUT);
  Serial.begin(9600);
  
  digitalWrite(X_DIR_PIN, LOW);

  // Move all the way across the long axis in the negative/low direction
  for(int x = 0; x < 8100; x++) {
    digitalWrite(X_STEP_PIN, HIGH);
    delayMicroseconds(PULSE_DUR);
    digitalWrite(X_STEP_PIN, LOW);
    delayMicroseconds(PULSE_DUR);
  }
  delay(1000); // One second delay

  digitalWrite(Z_DIR_PIN, LOW);

  // Move all the way across the short axis in the negative/low direction
  for(int x = 0; x < 5600; x++) {
    digitalWrite(Z_STEP_PIN, HIGH);
    delayMicroseconds(PULSE_DUR);
    digitalWrite(Z_STEP_PIN, LOW);
    delayMicroseconds(PULSE_DUR);
  }
  delay(1000); // One second delay
  digitalWrite(X_DIR_PIN, HIGH);
  
  // Move all the way across the long axis in the positive/high direction
  for(int x = 0; x < 8100; x++) {
    digitalWrite(X_STEP_PIN, HIGH);
    delayMicroseconds(PULSE_DUR);
    digitalWrite(X_STEP_PIN, LOW);
    delayMicroseconds(PULSE_DUR);
  }
  delay(1000); // One second delay
  digitalWrite(Z_DIR_PIN, HIGH);

  // Move all the way across the short axis in the positive/high direction
  for(int x = 0; x < 5600; x++) {
    digitalWrite(Z_STEP_PIN, HIGH);
    delayMicroseconds(PULSE_DUR);
    digitalWrite(Z_STEP_PIN, LOW);
    delayMicroseconds(PULSE_DUR);
  }
}

void loop() {
}
