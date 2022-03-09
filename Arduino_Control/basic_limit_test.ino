// https://forum.arduino.cc/t/using-end-stops-on-cnc-shield-design-for-gbrl/510231/2
int x_limit_switch_pin = 9;
int x_direction_switch_pin = 5;


void setup() {
  pinMode(x_limit_switch_pin, INPUT);  // sets the digital pin 13 as output
  pinMode(x_direction_switch_pin, OUTPUT);    // sets the digital pin 7 as input

}

void loop() {
   int val = digitalRead(x_limit_switch_pin);   // see if the pin is on
   Serial.print("HERE");
   if(val){
    Serial.print("Right limit hit");        // if it is on, print that the right limit is hit
   }
   digitalWrite(x_direction_switch_pin, 1);  // makes it indeed right
}
