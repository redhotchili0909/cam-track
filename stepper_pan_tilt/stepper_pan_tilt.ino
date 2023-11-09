#include <Adafruit_MotorShield.h>
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_StepperMotor *horMotor = AFMS.getStepper(200, 2);

String horInput;
int horMovement = 0;
int hPos = 0;

int fastThreshold = 150;
int fastMovement = 100;
int slowMovement = fastMovement / 2;

void setup() {
  Serial.begin(9600);
  horMotor->setSpeed(10); //10 rpm
}

void loop() {
  if (Serial.available() > 0) {
    horInput = Serial.readStringUntil('\n');
    horMovement = horInput.toInt();
    updatePosition(horMovement);
  }
}

void updatePosition(int horMovement) {
  /*
    Updates horizontal position of the stepper motor based
    on the horizontal input.

    Arguments:
      horMovement: integer reporting the distance (in pixels)
      of the center of the face from the center of the camera frame
  */
  if (horMovement == 0) {
    Serial.println("0");
    return;
  }

  if (abs(horMovement) > fastThreshold) {
    if (horMovement < 0) {
      horMotor->step(fastMovement, BACKWARD, SINGLE);
      Serial.println(-fastMovement);
    }
    else {
      horMotor->step(fastMovement, FORWARD, SINGLE);
      Serial.println(fastMovement);
    }
  }
  else {
    if (horMovement < 0) {
      horMotor->step(slowMovement, BACKWARD, SINGLE);
      Serial.println(-slowMovement);
    }
    else {
      horMotor->step(slowMovement, FORWARD, SINGLE);
      Serial.println(slowMovement);
    }
  }
}
