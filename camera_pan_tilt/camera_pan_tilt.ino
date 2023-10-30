# include <Servo.h>

// initialize Servo info
Servo horServo;
const int horPin = 8;
int hStart = 0;
int hPos = hStart;
String horInput;
int horMovement = 0;

void setup() {
  Serial.begin(9600);
  horServo.attach(horPin);
  horServo.write(hPos);
}

void loop() {
  if (Serial.available() > 0) {
    horInput = Serial.readStringUntil('\n');
    horMovement = horInput.toInt();

    updatePosition(horMovement);
    
    // check limits
    if (hPos > 180) {
      hPos = 180;
    }
    else if (hPos < 0) {
      hPos = 0;
    }

    horServo.write(hPos);
    Serial.println(hPos);
  }
}

void updatePosition(horMovement) {
  /*
    Updates horizontal position of the servo based on
    the input from the Raspberry Pi camera.

    Arguments:
      horMovement: integer reporting the distance (in pixels)
      of the center of the face from the center of the camera frame
  */
  if (horMovement == 0) {
      hPos += 0;
    } 
  else if (abs(horMovement) > 150) {
    if (horMovement < 0) {
          hPos +=10;
    }
    else {
      hPos -= 10;
    }
  }
  else {
    if (horMovement < 0) {
      hPos +=5;
    }
    else {
      hPos -= 5;
    }
  }
}
