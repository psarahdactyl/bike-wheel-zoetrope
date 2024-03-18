#include <AccelStepper.h>

#define BUTTON_PIN 12 // Change this to the pin your button is connected to
#define STEP_PIN 8
#define DIR_PIN 9
#define EN_DRIVE 10
#define EN 13
#define LED_PIN 11 // Change this to the pin your LED is connected to
#define DEBOUNCE_DELAY 50 // Debounce delay time

#define STEPS_PER_REV 6400  // Number of steps for one revolution
#define INITIAL_SPEED 0.0         // Initial speed in Hz
#define TARGET_SPEED 0.3          // Target speed in Hz (for sprocket or pulley)
// (TARGET_SPEED = num_bike_gear_teeth / num_sprocket_teeth * bike_wheel_target_speed in Hz) 
// so for bike chain -> 17/9 * 0.5 ~= 0.9
#define ACCELERATION 0.09        // Acceleration in Hz/s
#define DECELERATION -0.045      // Deceleration in Hz/s

enum { zoetropeIsOff, zoetropeIsOn, rampingUp, rampingDown };
unsigned char zoetropeState = zoetropeIsOff;
unsigned char zoetropeSpeed = 0;
unsigned long lastDebounceTime = 0;
bool buttonState = HIGH;
bool lastButtonState = HIGH;

float progress = 0;
float currentSpeed = 0;
unsigned long elapsedTime = 0;

unsigned long timerStartTime = 0; // Variable to hold the start time of the timer
const unsigned long timerDuration = 15000; // Duration of the timer in milliseconds (15 seconds)

// Create stepper motor object
AccelStepper stepper(AccelStepper::DRIVER, STEP_PIN, DIR_PIN);

void setup() {
    // motor stuff
  pinMode(EN_DRIVE, OUTPUT); 
  pinMode(EN, OUTPUT);
  pinMode(STEP_PIN, OUTPUT); 
  pinMode(DIR_PIN, OUTPUT);

  digitalWrite(DIR_PIN, LOW);

  // Set up the motor
  stepper.setMaxSpeed(TARGET_SPEED * STEPS_PER_REV);
  stepper.setAcceleration(ACCELERATION * STEPS_PER_REV);

  pinMode(BUTTON_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  static unsigned long startTime = 0;

  int reading = digitalRead(BUTTON_PIN);
  
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > DEBOUNCE_DELAY) {
    if (reading != buttonState) {
      buttonState = reading;

      if (buttonState == HIGH) {
        if (zoetropeState == zoetropeIsOff) {
          zoetropeState = rampingUp;
          timerStartTime = millis();
          digitalWrite(LED_PIN, LOW); // Turn on LED when zoetrope is ramping up
        } else if (zoetropeState == zoetropeIsOn) {
          zoetropeState = rampingDown;
          timerStartTime = millis();
          digitalWrite(LED_PIN, LOW); // Turn on LED when zoetrope is ramping up
        }
      }
    }
  }

  lastButtonState = reading;

  switch (zoetropeState) {
    case zoetropeIsOff:
      // disable motor
      digitalWrite(LED_PIN, HIGH); // Turn off LED when zoetrope is off
      digitalWrite(EN, LOW);
      break;

    case zoetropeIsOn:
      digitalWrite(EN, HIGH);
      digitalWrite(LED_PIN, LOW); // Turn on LED when zoetrope is on
      // Serial.println("on");
      // Serial.println(TARGET_SPEED * STEPS_PER_REV);
      stepper.setSpeed(TARGET_SPEED * STEPS_PER_REV);
      stepper.runSpeed();
      break;

    case rampingUp:
      elapsedTime = millis() - timerStartTime;
      digitalWrite(EN, HIGH);
      digitalWrite(LED_PIN, LOW); // Turn on LED when zoetrope is on
      if (elapsedTime < timerDuration) {
        progress = elapsedTime / timerDuration; // ramp up in 15 seconds
        currentSpeed = INITIAL_SPEED + progress * (TARGET_SPEED - INITIAL_SPEED);
        stepper.setSpeed(currentSpeed * STEPS_PER_REV);
        stepper.runSpeed();
        // Serial.println(currentSpeed,10);
        // Serial.println(TARGET_SPEED,10);
        // Serial.println(elapsedTime);
      } 
      else {
        zoetropeState = zoetropeIsOn;
      }
      break;

    case rampingDown:
      elapsedTime = millis() - timerStartTime;
      digitalWrite(EN, HIGH);
      digitalWrite(LED_PIN, LOW); // Turn on LED when zoetrope is on
      if (elapsedTime < timerDuration) {
        // Serial.println("ramping down");
        progress = elapsedTime / timerDuration;
        currentSpeed = TARGET_SPEED + progress * (DECELERATION - TARGET_SPEED);
        stepper.setSpeed(currentSpeed * STEPS_PER_REV);
        stepper.runSpeed();
      } else {
        zoetropeState = zoetropeIsOff;
        digitalWrite(LED_PIN, HIGH); // Turn off LED when zoetrope is off
      }
      break;
  }
  // Serial.println(zoetropeState);

}
