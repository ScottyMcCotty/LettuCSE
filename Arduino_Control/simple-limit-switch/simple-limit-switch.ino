// https://forum.arduino.cc/t/using-end-stops-on-cnc-shield-design-for-gbrl/510231/2
int x_limit_switch_pin = 10;
int count = 0;

void setup() {
  pinMode(x_limit_switch_pin, INPUT_PULLUP);
  Serial.begin(9600);
  delay(500);
}

void loop() {
  int val = digitalRead(x_limit_switch_pin);
  if (val == LOW) {
    count++;
    Serial.print("Press me harder, daddy x"); Serial.println(count);
    delay(100);
  }
}
