int VRx = A0;
int VRy = A1;
int SW = 2;

int xPosition = 0;
int yPosition = 0;
int SW_state = 0;
int inX = 0;
int inY = 0;

const int CALIBRATION_SIZE = 100;
//int xCalibrations[CALIBRATION_SIZE];
//int yCalibrations[CALIBRATION_SIZE];

int xBias = 0;
int yBias = 0;

void setup() {
  Serial.begin(115200); 
  
  pinMode(VRx, INPUT);
  pinMode(VRy, INPUT);
  pinMode(SW, INPUT_PULLUP);

  delay(200);

  calculateBias();
}

void loop() {
  xPosition = analogRead(VRx);
  yPosition = analogRead(VRy);
  SW_state = digitalRead(SW);

  inX = doScaling(xPosition, xBias);
  inY = doScaling(yPosition, yBias);
  
  Serial.print("X: ");
  Serial.print(inX);
  Serial.print(" | Y: ");
  Serial.print(inY);
  Serial.print(" | Button: ");
  Serial.println(SW_state);

//  Serial.println(inX);

  delay(30);
  
}

int doScaling(int value, int bias) {

  // return the value without the bias
  return value - bias;
  
  // simple mapping
//  return map(value, 0, 1023, -512, 512);

  // using square root
//  return sqrt(value);

//  return value;
}

void calculateBias() {

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

//  Serial.print("X: total= "); Serial.print(xValues);
//  Serial.print(" | avg= "); Serial.print(xAvg);
//  Serial.print(" | bias= "); Serial.print(xBias);
//  Serial.print(" | ("); Serial.print(CALIBRATION_SIZE); Serial.println(" values)");
//  Serial.print("Y: total= "); Serial.print(yValues); 
//  Serial.print(" | avg= "); Serial.print(yAvg);
//  Serial.print(" | bias= "); Serial.print(yBias);
//  Serial.print(" | ("); Serial.print(CALIBRATION_SIZE); Serial.println(" values)");
}
