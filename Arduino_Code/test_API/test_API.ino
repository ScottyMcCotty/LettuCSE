

// define pin constants
#define RED_PIN 8
#define BLUE_PIN 2
#define DELAY_DURATION 500
#define ON_DURATION 1000

long red_start_time = 0;
long blue_start_time = 0;
bool string_complete = false;
bool red_is_on = false;
bool blue_is_on = false;
String input = "";

void setup() {
  // do nothing
  Serial.begin(9600);
  pinMode(RED_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  delay(50);
  Serial.println("Valid client instructions:\n  red\n  blue\n  purple\n");
}

void loop() {

  if (string_complete) {
    string_complete = false;

    if (input == "red") {
      redOn();
      red_start_time = millis();
    }
    else if (input == "blue") {
      blueOn();
      blue_start_time = millis();
    }
    else if (input == "purple") {
      purpleOn();
      red_start_time = millis();
      blue_start_time = millis();
    }
    else {
      Serial.println("What are you doing? '" + input + "' isn't a known command");
    }

    // reset the input string
    input = "";
  }

  if (red_is_on && millis() - red_start_time >= ON_DURATION) {
    redOff();
    Serial.println("Success. Red LED now off");
  }
  if (blue_is_on && millis() - blue_start_time >= ON_DURATION) {
    blueOff();
    Serial.println("Success. Blue LED now off");
  }


// just testing the functions

//  redOn();
//  delay(DELAY_DURATION);
//  
//  redOff();
//  delay(DELAY_DURATION);
//
//  blueOn();
//  delay(DELAY_DURATION);
//
//  blueOff();
//  delay(DELAY_DURATION);
//
//  purpleOn();
//  delay(DELAY_DURATION);
//
//  purpleOff();
//  delay(DELAY_DURATION);
}

/*
  SerialEvent occurs whenever a new data comes in the hardware serial RX. This
  routine is run between each time loop() runs, so using delay inside loop can
  delay response. Multiple bytes of data may be available.
*/
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      string_complete = true;
    }
    else {
      // otherwise, add it to the inputString:
      input += inChar;
    }
  }
}

void redOn() {
  // turn red LED on
  digitalWrite(RED_PIN, HIGH);
  red_is_on = true;
}

void redOff() {
  // turn red LED off
  digitalWrite(RED_PIN, LOW);
  red_is_on = false;
}

void blueOn() {
  // turn blue LED on
  digitalWrite(BLUE_PIN, HIGH);
  blue_is_on = true;
}

void blueOff() {
  // turn blue LED off
  digitalWrite(BLUE_PIN, LOW);
  blue_is_off = false;
}

void purpleOn() {
  // turn red and blue LEDs on
  redOn();
  blueOn();
}

void purpleOff() {
  // turn red and blue LEDs off
  redOff();
  blueOff();
}
