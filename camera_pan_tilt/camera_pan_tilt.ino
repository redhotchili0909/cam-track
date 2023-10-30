# include <Servo.h>

// initialize Servo info
Servo horServo;
const int horPin = 8;
int hPos = hStart;
int hStart = 50;
int horMovement = 0;

void setup() {
  Serial.begin(9600);
  horServo.attach(horPin);
  horServo.write(hPos);
}

void loop() {
  if (Serial.available() > 0) {
    // check serial message from raspi to see which way to move
    horMovement = Serial.parseInt();
    // change horMovement to some distance for servo to move
    hPos = hPos + horMovement;
  }
  Serial.println(horMovement);
  horServo.write(hPos);

}
