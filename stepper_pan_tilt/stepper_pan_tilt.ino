const int stepXPin = 2; //X.STEP
const int dirXPin = 5; // X.DIR

String xInput;
int xMovement = 0;
int xPos = 0;

int fastThreshold = 150;
int fastMovementDelay = 1000;
int slowMovementDelay = fastMovementDelay / 2;

const int stepsPerRev = 200;
int pulseWidthMicros = 100;  // microseconds
int millisBtwnSteps = slowMovementDelay;

void setup() {
  Serial.begin(9600);
  pinMode(stepXPin, OUTPUT);
  pinMode(dirXPin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    // read x input from pi
    xInput = Serial.readStringUntil('\n');
    // convert to integer
    xMovement = xInput.toInt();

    if (xMovement != 0) {
      // if xMovement isn't 0, move stepper
      updatePosition(xMovement);
      for (int i = 0; i < stepsPerRev; i++) {
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(pulseWidthMicros);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(millisBtwnSteps);
      }
    }
  }
}

void updatePosition(int xMovement) {
  /*
    Updates horizontal position of the stepper motor based
    on the horizontal input.

    Arguments:
      xMovement: integer reporting the distance (in pixels)
      of the center of the face from the center of the camera frame
  */

  if (xMovement < 0) {
    // move left; go clockwise
    digitalWrite(dirPin, HIGH);
  }
  else {
    digitalWrite(dirPin, LOW);
  }

  if (abs(xMovement) > fastThreshold) {
    millisBtwnSteps = fastMovementDelay;
  }
  else {
    millisBtwnSteps = slowMovementDelay;
  }
}
