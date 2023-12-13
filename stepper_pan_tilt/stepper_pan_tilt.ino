const int X_STEP_PIN = 2; //X.STEP
const int X_DIR_PIN = 5; // X.DIR
const int Y_STEP_PIN = 3; //Y.STEP
const int Y_DIR_PIN = 6; // Y.DIR

String inputDist;
int xDist = 0;
int yDist = 0;

const int fastThreshold = 200;
int fastMovementDelay = 500;
int slowMovementDelay = fastMovementDelay * 2;
int millisBtwnSteps = slowMovementDelay;
int stepsPerRound = 0;
int xSteps = 0;
int ySteps = 0;

int xStepDividend = 10;
int yStepDividend = 10;

unsigned long start_millis;
unsigned long current_millis;
unsigned long stop_period = 4000;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(50);
  pinMode(X_STEP_PIN, OUTPUT);
  pinMode(X_DIR_PIN, OUTPUT);
  pinMode(Y_STEP_PIN, OUTPUT);
  pinMode(Y_DIR_PIN, OUTPUT);
}

void loop() {
  start_millis = millis();

  if (Serial.available() > 0) {
    // read x input from pi
    inputDist = Serial.readStringUntil('\n');
    // Serial.println(inputDist);
    parseDistInput(inputDist);
    Serial.println(inputDist);
    
    updateXMovement(xDist);
    updateYMovement(yDist);

    // steps for each loop
    stepsPerRound = max(xSteps, ySteps);

    for (int i = 0; i < stepsPerRound; i++) {
      // each motor goes high for some millisBtwnSteps,
      // goes low after so it makes one step at a time
      // for stepsPerRound
      if (i < xSteps) {
        // if x took xSteps already, don't set high again
        digitalWrite(X_STEP_PIN, HIGH);
      }
      if (i < ySteps) {
        // if y took ySteps already, don't set high again
        digitalWrite(Y_STEP_PIN, HIGH);
      }
      delayMicroseconds(millisBtwnSteps);
      digitalWrite(X_STEP_PIN, LOW);
      digitalWrite(Y_STEP_PIN, LOW);
      delayMicroseconds(millisBtwnSteps);
    }
  }
  // Serial.print(xSteps);
  // Serial.print(",");
  // Serial.println(ySteps);

  // ready handshake
  // Serial.println(1);

  // current_millis = millis();
  // if (current_millis - start_millis > stop_period) {
  //   // stop stepper

  // }

}

void parseDistInput(String inputDist) {
  /*
    Parses string distance input from Serial Monitor into x and y distances.
    Argument: 
      inputDist: String input from Raspberry Pi relating how far
      the current x and y coordinates are from the center of the frame
      in the format: 'x,y'
  */
  String xDistInput = inputDist.substring(0, inputDist.indexOf(","));
  String yDistInput = inputDist.substring(inputDist.indexOf(",") + 1, inputDist.length());
  xDist = xDistInput.toInt();
  yDist = yDistInput.toInt();
}

void updateXMovement(int xDist) {
  /*
    Updates direction, speed, and number of steps to take 
    for the horizontal stepper motor based on the horizontal
    distance from the subject.

    Arguments:
      xDist: integer reporting the distance (in pixels) of the
      center of the subject from the center of the camera frame
  */
  
  xSteps = abs(xDist) / xStepDividend;

  if (xDist < 0) {
    // move left; go clockwise
    digitalWrite(X_DIR_PIN, HIGH);
  }
  else {
    digitalWrite(X_DIR_PIN, LOW);
  }

  if (abs(xDist) > fastThreshold) {
    millisBtwnSteps = fastMovementDelay;
  }
  else {
    millisBtwnSteps = slowMovementDelay;
  }
}

void updateYMovement(int yDist) {
  /*
    Updates direction, speed, and number of steps to take 
    for the vertical stepper motor based on the vertical
    distance from the subject.

    Arguments:
      yDist: integer reporting the distance (in pixels) of the
      center of the subject from the center of the camera frame
  */

  ySteps = abs(yDist) / yStepDividend;

  if (yDist < 0) {
    // move down; go clockwise
    digitalWrite(Y_DIR_PIN, LOW);
  }
  else {
    digitalWrite(Y_DIR_PIN, HIGH);
  }

  if (abs(yDist) > fastThreshold) {
    millisBtwnSteps = fastMovementDelay;
  }
  else {
    millisBtwnSteps = slowMovementDelay;
  }
}
