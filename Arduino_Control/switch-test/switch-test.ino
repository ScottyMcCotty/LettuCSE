

const int X_STOP = 9;

void setup() {
  // put your setup code here, to run once:

  pinMode(X_STOP, INPUT_PULLUP);
  Serial.begin(9600);

  delay(500);
}

void loop() {
  // put your main code here, to run repeatedly:


  int val = digitalRead(X_STOP);
  Serial.print("Pin: "); Serial.println(val);

  delay(200);
}
