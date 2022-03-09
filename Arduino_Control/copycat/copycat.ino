

String input = "";
bool string_complete = false;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  delay(500); // delay half a second, for good measure
}

void loop() {

  if (string_complete) {
    string_complete = false;

    String message = "You told me: '" + input + "'";
    input = "";

    Serial.println(message);
  }
}


void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();

    if (inChar == '\n') {
      string_complete = true;
    }
    else {
      input += inChar;
    }
  }
}
