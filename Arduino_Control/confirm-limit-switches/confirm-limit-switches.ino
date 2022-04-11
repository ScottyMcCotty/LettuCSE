
const int Z_STOP_NEG = 11;
const int Z_STOP_POS = 6;

void setup() {
  // put your setup code here, to run once:
  pinMode(Z_STOP_NEG, INPUT_PULLUP);
  pinMode(Z_STOP_POS, INPUT_PULLUP);
  Serial.begin(115200);
  delay(300);
}

void loop() {
  // put your main code here, to run repeatedly:

  Serial.print("NEG: "); Serial.print(digitalRead(Z_STOP_NEG));
  Serial.print(" | POS: "); Serial.println(digitalRead(Z_STOP_POS));
  delay(200);
}
