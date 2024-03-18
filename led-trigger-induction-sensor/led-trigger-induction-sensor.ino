#define ledPin 12
#define sensorPin 13

static unsigned long TriggeredTime = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(sensorPin,INPUT); 
  pinMode(ledPin,OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

  while (!digitalRead(sensorPin));
  unsigned long elapsedTime = millis() - TriggeredTime;
  TriggeredTime - millis();
  Serial.println(elapsedTime);
  digitalWrite(ledPin, HIGH);
  delayMicroseconds(1000);
  digitalWrite(ledPin, LOW);
  while (digitalRead(sensorPin));

}
