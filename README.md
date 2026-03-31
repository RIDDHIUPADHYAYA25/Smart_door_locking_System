🏠 Smart Home Security System Using Face Recognition

This project implements an AI-powered smart door security system that combines Face Recognition, Arduino automation, and motion detection to enhance home safety.

The system identifies whether the person at the door is known or unknown and takes appropriate actions such as opening the door automatically or sending an email alert with a captured image.

🎯 Project Objective

The goal of this project is to build an intelligent home security system that:

Automatically recognizes authorized persons
Opens the door using a servo motor for known people
Detects if someone is inside the home using a PIR sensor
Captures and sends images of unknown visitors when no one is inside
Provides real-time alerts to the homeowner via email
⚙️ System Workflow

1️⃣ User presses the switch to activate the system.

2️⃣ Laptop camera captures the face of the visitor.

3️⃣ DeepFace library compares the face with stored images in the dataset.

4️⃣ If the face is recognized:

Python sends an OPEN command to Arduino
Arduino activates the servo motor
The door opens automatically

5️⃣ If the face is unknown:

Arduino checks the PIR sensor

6️⃣ If PIR detects no motion inside the house:

System captures the visitor's image
Sends an email alert with the photo

7️⃣ If motion is detected inside the house:

No email is sent

8️⃣ The system resets and waits for the next visitor

🧩 Hardware Components
Arduino Uno
PIR Motion Sensor
Servo Motor
Push Button Switch
Jumper Wires
Laptop Camera (for face recognition)

💻 Software & Libraries
Python
Arduino IDE
OpenCV
DeepFace
PySerial
SMTP (Email sending)

Install required libraries:

pip install opencv-python
pip install deepface
pip install pyserial

🔌 Circuit Connections
Component	Arduino Pin
PIR Sensor OUT	D2
Switch	D3
Servo Signal	D9
VCC	5V
GND	GND

📸 Features

✔ Face Recognition using AI
✔ Automatic Door Opening
✔ Motion Detection with PIR
✔ Email Alert with Image Attachment
✔ Laptop Camera Integration
✔ Arduino-Python Serial Communication

🚀 Future Improvements
Mobile app integration
IoT cloud monitoring
ESP32-CAM implementation
WhatsApp or SMS alerts
Multiple camera support
🔒 Applications
Smart Home Security
Office Access Control
Apartment Security
Hostel Entry Monitoring
👩‍💻 Author

Riddhi Upadhyaya
B.Tech CSE Student
Project: AI Based Smart Home Security System
