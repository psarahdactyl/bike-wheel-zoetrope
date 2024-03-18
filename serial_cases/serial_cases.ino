#define ledPin 12
#define sensorPin 13

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(sensorPin,INPUT); 
  pinMode(ledPin,OUTPUT);
}

unsigned long previousTime = 0;
unsigned long timeNow;
unsigned long elapsedTime;
int frame;

void loop() {

  // put your main code here, to run repeatedly:
  while (!digitalRead(sensorPin));
  timeNow = millis();
  elapsedTime = timeNow - previousTime;
  //digitalWrite(ledPin, HIGH);
  delayMicroseconds(1000);
  //digitalWrite(ledPin, LOW);
  previousTime = timeNow;
  //Serial.println(elapsedTime);

  if (elapsedTime < 40){
  Serial.println("F1");
  frame = 0;
  Serial.println(frame);

  }
  else{
    frame++;
    Serial.println(frame);

  }

  while (digitalRead(sensorPin));



  // else:
    // Serial.write("NF")

}
