String input_dist;
int dist_away = 0;

#include <Servo.h>

Servo driving_motor;

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  driving_motor.attach(9);  

  esc_calibrate(driving_motor);
}

void loop() {  

  // if (Serial.available() > 0) {
  //   input_dist = Serial.readStringUntil('\n');
  //   dist_away = input_dist.toInt();
  digitalWrite(LED_BUILTIN, HIGH);
  set_esc_power(driving_motor, 50);

}

void set_esc_power (Servo motor, int power){
  power = constrain(power, -100, 100);
  int signal_min = 1050;
  int signal_max = 1950;
  int signal_output = map(power, -100, 100, signal_min, signal_max); //map(value, fromLow, fromHigh, toLow, toHigh)
  motor.writeMicroseconds(signal_output);
}

void esc_calibrate (Servo motor) {
  // calibration: hit reset on arduino, plug in, wait for the beeps 
  digitalWrite(LED_BUILTIN, HIGH);
  set_esc_power(motor, 100);  
  delay(5000);
  digitalWrite(LED_BUILTIN, LOW);
  set_esc_power(motor, 0);
  delay(5000);
}
