#include  <Wire.h>
#include  <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27,16,2);  // set the LCD address to 0x27 for a 16 chars and 2 line display

void setup()
{
  lcd.init();                      // initialize the lcd 
  lcd.backlight();
  Serial.begin(9600);
}

void loop()
{
  // when characters arrive over the serial port...
  if (Serial.available()) {
    
    // wait a bit for the entire message to arrive
    delay(100);

    
    
    // clear the screen
    lcd.clear();
    // read all the available characters
    String line = "";
    while (Serial.available() > 0) {
      char ch = Serial.read();
      if (ch != '\n') line += ch;
//      // display each character to the LCD
//      lcd.write(Serial.read());
    }

    int index = line.indexOf(" ");
    String x = line.substring(0, index);
    String y = line.substring(index+1);

    char x_str[10];
    char y_str[10];
    x.toCharArray(x_str, 10);
    y.toCharArray(y_str, 10);
//    char str[10];
//    line.toCharArray(str, 10);
//    lcd.printstr(str);
    lcd.setCursor(0, 0);
    lcd.printstr("    X:  ");
    lcd.printstr(x_str);
    lcd.setCursor(0, 1);
    lcd.printstr("    Y:  ");
    lcd.printstr(y_str);
  }
}
