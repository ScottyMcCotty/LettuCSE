//
// Transplanting Toolhead Arduino Firmware
// 2022-04-22
//
// Pin setup:
// - Digital pins 2, 5 (X-motor connections): Step and direction pins
// - Digital pin  9 (X-axis limit switch): lead screw bottom limit switch
// - Digital pin 10 (Y-axis limit switch): fork limit switch
// - Digital pin 11 (Z-axis limit switch): lead screw top limit switch
//
// Limit switch pins are configured with pull up resistors and are normally open,
// so LOW means the switch is not pressed and HIGH means the switch is pressed
//


const int STEP_PIN = 2;
const int DIR_PIN = 5;

const int SCREW_BOT_LIMIT = 9;
const int FORK_LIMIT = 10;
const int SCREW_TOP_LIMIT = 11;

const int HALF_PERIOD = 600; // microseconds

const int UP = 0;
const int DOWN = 1;
const String UP_STRING = "0";
const String DOWN_STRING = "1";


//
// Main procedures
//

void setup() {
  set_up_pins();
  set_up_serial();
}

void loop() {
  String input = wait_for_input("Toolhead command? ");

  if (input == UP_STRING) {
    Serial.println("moving up");
    move(UP);
  } else if (input == DOWN_STRING) {
    Serial.println("moving down");
    move(DOWN);
  } else {
    Serial.println("Failed! Unknown command");
    while(1){} // block forever
  }
}


//
// Helper functions
//

void move(int dir) {
  digitalWrite(DIR_PIN, dir);
  for (;;) {
    if (dir == UP && !can_move_up()) {
      Serial.println("hit top");
      return;
    }
    if (dir == DOWN && !can_move_down()) {
      Serial.println("hit bottom");
      return;
    }

    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(HALF_PERIOD);
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(HALF_PERIOD);
  }
}

String wait_for_input(String prompt) {
  int state = 0;
  char buf[] = {'\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0',
                '\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0'};

  while (state == 0) {
    state = Serial.readBytesUntil('\n', buf, 20);
  }

  return String(buf);
}

void set_up_pins() {
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(SCREW_BOT_LIMIT, INPUT_PULLUP);
  pinMode(FORK_LIMIT, INPUT_PULLUP);
  pinMode(SCREW_TOP_LIMIT, INPUT_PULLUP);
}

void set_up_serial() {
  Serial.begin(9600);
  delay(500);
  Serial.println("Hello, world!");
}

boolean can_move_up() {
  return digitalRead(SCREW_TOP_LIMIT) == HIGH;
}

boolean can_move_down() {
  return digitalRead(SCREW_BOT_LIMIT) == HIGH && digitalRead(FORK_LIMIT) == HIGH;
}
