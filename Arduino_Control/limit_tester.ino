 
// https://forum.arduino.cc/t/using-end-stops-on-cnc-shield-design-for-gbrl/510231/2
int x_limit_switch_pin = 9;
//int x_direction_switch_pin = 5;


void setup() {
  Serial.begin(9600);
  pinMode(x_limit_switch_pin, INPUT_PULLUP);  // sets the digital pin 13 as output

}

void loop() {
   int val = digitalRead(x_limit_switch_pin);   // see if the pin is on
   if(val==LOW){
    Serial.print("Right limit hit");        // if it is on, print that the right limit is hit
   }
   delay(300);
   //digitalWrite(x_direction_switch_pin, 1);  // makes it indeed right
}
