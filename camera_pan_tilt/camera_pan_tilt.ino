# include <Servo.h>

// initialize Servo info
Servo horServo;
const int horPin = 8;
int hStart = 50;
int hPos = hStart;
String horMovement;
int horMovementNum = 0;

void setup() {
  Serial.begin(9600);
  horServo.attach(horPin);
  horServo.write(hPos);
}

void loop() {
  if (Serial.available() > 0) {
    // check serial message from raspi to see which way to move
    horMovement = Serial.readStringUntil('\n');
    // change horMovement to some distance for servo to move
    horMovementNum = horMovement.toInt();
    hPos = hPos + horMovementNum;
    Serial.println(horMovement);
  }
  horServo.write(hPos);

}
