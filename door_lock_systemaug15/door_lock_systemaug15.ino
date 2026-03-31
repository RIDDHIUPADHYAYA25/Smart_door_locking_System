#include <Servo.h>

// Pin definitions
const int pirPin = 2;      // PIR sensor OUT → D2
const int ledPin = 8;      // LED (+) → D8
const int servoPin = 9;    // Servo signal → D9

Servo doorServo;
bool doorOpen = false;       // Track servo state
bool motionDetected = false; // PIR status

void setup() {
  Serial.begin(9600);
  pinMode(pirPin, INPUT);
  pinMode(ledPin, OUTPUT);

  doorServo.attach(servoPin);
  doorServo.write(0); // Door starts closed

  Serial.println("Arduino Ready");
}

void loop() {
  // Continuously monitor PIR
  motionDetected = false;
  for (int i = 0; i < 5; i++) {   // Read PIR multiple times quickly
    if (digitalRead(pirPin) == HIGH) {
      motionDetected = true;
      break;
    }
    delay(50);
  }

  // Handle serial commands from Python
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    Serial.print("Received: "); Serial.println(command);

    if (command == "OPEN" && !doorOpen) {
      openDoor();
      digitalWrite(ledPin, HIGH);  // LED ON for known person
      delay(500);
      digitalWrite(ledPin, LOW);
    }
    else if (command == "CHECK") {
      // Immediately respond with current PIR status
      Serial.println(motionDetected ? "MOTION" : "NO_MOTION");
    }
  }
}

void openDoor() {
  doorOpen = true;         
  Serial.println("Opening door...");
  doorServo.write(90);     // Open door
  delay(3000);             // Keep door open
  doorServo.write(0);      // Close door
  doorOpen = false;        
  Serial.println("Door closed");
}