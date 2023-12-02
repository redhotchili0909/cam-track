#include <Servo.h>

Servo driving_motor;
const int driving_motor_pin = 9;

void setup() {
  driving_motor.attach(driving_motor_pin);
}

void loop() {
  // put your main code here, to run repeatedly:
  set_motor_power(driving_motor, 100);
}

void set_motor_power (Servo motor, int power) {
  power = constrain(power, -100, 100);
  // min and max pwm signal length, figure this out for our motor
  int signal_min = 1050;
  int signal_max = 1950;
  // maps -100 to 100 (power input) to the actual signal min and maxes
  // for easier calculations
  int signal_output = map(power, -100, 100, signal_min, signal_max);
  motor.writeMicroseconds(signal_output);
}