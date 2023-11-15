const int X_STEP_PIN = 2; //X.STEP
const int X_DIR_PIN = 5; // X.DIR
const int Y_STEP_PIN = 3; //X.STEP
const int Y_DIR_PIN = 6; // X.DIR

String xInput;
int xMovement = 0;
int xPos = 0;

String yInput;
int yMovement = 0;
int yPos = 0;

int fastThreshold = 150;
int fastMovementDelay = 1000;
int slowMovementDelay = fastMovementDelay / 2;

const int stepsPerRev = 200;
// int pulseWidthMicros = 100;  // microseconds
int millisBtwnSteps = slowMovementDelay;

void setup() {
  Serial.begin(9600);
  pinMode(X_STEP_PIN, OUTPUT);
  pinMode(X_DIR_PIN, OUTPUT);
  pinMode(Y_STEP_PIN, OUTPUT);
  pinMode(Y_DIR_PIN, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    // read x input from pi
    xInput = Serial.readStringUntil('\n');
    // convert to integer
    xMovement = xInput.toInt();
    yMovement = xInput.toInt();

    if (xMovement != 0 | yMovement != 0) {
      // if xMovement isn't 0, move stepper
      updateXPosition(xMovement);
      updateYPosition(yMovement);
      for (int i = 0; i < stepsPerRev; i++) {
        digitalWrite(X_STEP_PIN, HIGH);
        digitalWrite(Y_STEP_PIN, HIGH);
        delayMicroseconds(millisBtwnSteps);
        digitalWrite(X_STEP_PIN, LOW);
        digitalWrite(Y_STEP_PIN, LOW);
        delayMicroseconds(millisBtwnSteps);
      }
    }
  }
}

void updateXPosition(int xMovement) {
  /*
    Updates horizontal position of the stepper motor based
    on the horizontal input.

    Arguments:
      xMovement: integer reporting the distance (in pixels)
      of the center of the face from the center of the camera frame
  */
  if (xMovement == 0) {
    return;
  }

  if (xMovement < 0) {
    // move left; go clockwise
    digitalWrite(X_DIR_PIN, HIGH);
  }
  else {
    digitalWrite(X_DIR_PIN, LOW);
  }

  if (abs(xMovement) > fastThreshold) {
    millisBtwnSteps = fastMovementDelay;
  }
  else {
    millisBtwnSteps = slowMovementDelay;
  }
}

void updateYPosition(int yMovement) {
  /*
    Updates vertical position of the stepper motor based
    on the vertical input.

    Arguments:
      yMovement: integer reporting the distance (in pixels)
      of the center of the face from the center of the camera frame
  */

  if (yMovement == 0) {
    return;
  }

  if (yMovement < 0) {
    // move left; go clockwise
    digitalWrite(Y_DIR_PIN, HIGH);
  }
  else {
    digitalWrite(Y_DIR_PIN, LOW);
  }

  if (abs(yMovement) > fastThreshold) {
    millisBtwnSteps = fastMovementDelay;
  }
  else {
    millisBtwnSteps = slowMovementDelay;
  }
}
