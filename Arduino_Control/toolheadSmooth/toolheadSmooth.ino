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
const String CALIBRATE_STRING = "calibrate";

const double TARGET = 600.0; // delay at highest (target) speed
const double START = 1600.0;  // delay at starting speed
const int STEPS_TO_MAX_SPEED = 600;
int delays[STEPS_TO_MAX_SPEED] = {1100};

//
// Main procedures
//

void setup() {
  set_up_pins();
  populate_delay_array();
  set_up_serial();
}

void loop() {
  String input = wait_for_input("Toolhead command? ");

  if (input == UP_STRING || input == CALIBRATE_STRING) {
//    Serial.println("moving up");
//    move(UP);
    smooth(UP);
  } else if (input == DOWN_STRING) {
//    Serial.println("moving down");
    move(DOWN);
  } else {
    Serial.println("Failed! Unknown command");
    while(1){} // block forever
  }
}


//
// Helper functions
//

void smooth(int dir) {
  digitalWrite(DIR_PIN, dir);

  int counter = 0;
  int pulse = HIGH;
  unsigned long previous = micros();
  
  while (counter < STEPS_TO_MAX_SPEED) {
    if (dir == UP && !can_move_up()) {
      Serial.println("Done");
      return;
    }
    if (dir == DOWN && !can_move_down()) {
      Serial.println("Done");
      return;
    }

    unsigned long current = micros();
    if (current - previous > delays[counter]) {
      digitalWrite(STEP_PIN, pulse);
      if (pulse == LOW) {
        counter++;
      }
      pulse = (pulse + 1) % 2;
      previous = current;
    }
  }
  move(dir);
}


void move(int dir) {
  digitalWrite(DIR_PIN, dir);
  for (;;) {
    if (dir == UP && !can_move_up()) {
      Serial.println("Done");
      return;
    }
    if (dir == DOWN && !can_move_down()) {
      Serial.println("Done");
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

void populate_delay_array() {
  const double m = (1.0 - (TARGET / START)) / (TARGET * STEPS_TO_MAX_SPEED);
  const double b = 1.0 / START;

  for (int ii = 0; ii < STEPS_TO_MAX_SPEED; ++ii) {
    double p = 1.0 / (m * ii + b);
    delays[ii] = int(p);
  }
}
