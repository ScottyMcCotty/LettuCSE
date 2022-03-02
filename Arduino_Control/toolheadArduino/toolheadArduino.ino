

void setup() {
  // put your setup code here, to run once:

  //TODO: pinMode setup goes here
  //TODO: Serial.begin(baudrate) & delay(500), unless other method needed
  //      to initialize toolhead Arduino

}

void loop() {
  // Continue after receiving input
  int input = wait_for_input("Toolhead command? ").toInt();

  // Call the relevant movement commands based on input
  switch(input) {
    case 1: // grab_plant: lower toolhead, then grab
      toolhead_lower();
      toolhead_grab();
      Serial.println("Down");
      break;
    case 2: // release_plant: release, then raise toolhead
      toolhead_release();
      toolhead_raise();
      Serial.println("Up");
      break;
    default: // unrecognized command
      Serial.println("Error");
      break;
  }
}

// Scott's (cleaned up) function to pause until input (terminated with \n) is received
String wait_for_input(String prompt) {
  int state = 0;
  int count = 0;
  char buf[] = {'\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0',
                '\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0', '\0'};

  while (state == 0) {
    state = Serial.readBytesUntil('\n', buf, 20);
  }

  return String(buf);
}

// TOOLHEAD MOVEMENT FUNCTIONS

void toolhead_lower() {
  //TODO: Implement based on toolhead motor movement commands
}

void toolhead_raise() {
  //TODO: Implement based on toolhead motor movement commands
}

void toolhead_grab() {
  //TODO: Implement based on toolhead motor movement commands
}

void toolhead_release() {
  //TODO: Implement based on toolhead motor movement commands
}
