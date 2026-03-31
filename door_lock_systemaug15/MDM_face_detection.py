import cv2
from deepface import DeepFace
import os
import serial
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# ===== Arduino Serial Connection =====
arduino_port = "COM6"  # Replace with your COM port
baud_rate = 9600

arduino = None
while arduino is None:
    try:
        arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
        time.sleep(2)
        print("Arduino connected")
    except Exception as e:
        print("Waiting for Arduino...", e)
        time.sleep(2)

# ===== Email Setup =====
EMAIL_ADDRESS = "riddhiupadhyaya2005@gmail.com"
EMAIL_PASSWORD = "nmet pduq wdpj isga"  # App password
TO_EMAIL = "riddhiupadhyaya2005@gmail.com"

def send_email(subject, body, image_path=None):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject

    # Add text body
    msg.attach(MIMEText(body, "plain"))

    # Attach image file
    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f'attachment; filename="{os.path.basename(image_path)}"'
        )
        msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())

# ===== Load Known Faces =====
known_faces_folder = "known_people"
known_faces = []
known_names = []

for filename in os.listdir(known_faces_folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        img_path = os.path.join(known_faces_folder, filename)
        known_faces.append(img_path)
        known_names.append(os.path.splitext(filename)[0])

# ===== Camera Setup =====
cap = cv2.VideoCapture(0)
last_identity = None
stable_count = 0
STABILITY_THRESHOLD = 5
door_triggered = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        detections = DeepFace.extract_faces(frame, enforce_detection=False)
        if detections:
            for det in detections:
                facial_area = det['facial_area']
                x, y, w, h = facial_area['x'], facial_area['y'], facial_area['w'], facial_area['h']
                face_img = frame[y:y + h, x:x + w]

                identity = "Unknown"
                for idx, known_face_path in enumerate(known_faces):
                    try:
                        result = DeepFace.verify(face_img, known_face_path, enforce_detection=False)
                        if result["verified"]:
                            identity = known_names[idx]
                            break
                    except:
                        continue

                # Stability check
                if identity == last_identity:
                    stable_count += 1
                else:
                    stable_count = 0
                last_identity = identity

                # Trigger Arduino only when stable
                if stable_count >= STABILITY_THRESHOLD:
                    if identity != "Unknown" and not door_triggered:
                        print(f"[INFO] Known person detected: {identity}")
                        try:
                            arduino.write(b'OPEN\n')
                            time.sleep(0.2)
                            door_triggered = True  # prevent repeated command
                        except Exception as e:
                            print("Error sending OPEN command:", e)
                    elif identity == "Unknown":
                        door_triggered = False  # reset for next detection
                        try:
                            arduino.write(b'CHECK\n')
                            time.sleep(0.2)
                            pir_status = arduino.readline().decode().strip()
                            print(f"[INFO] PIR status: {pir_status}")

                            if pir_status == "NO_MOTION":
                                # Capture unknown person image
                                img_name = f"unknown_{int(time.time())}.jpg"
                                cv2.imwrite(img_name, face_img)

                                # Send email alert
                                send_email(
                                    "Unknown Person Alert",
                                    "An unknown person was detected outside your home while no one is inside.",
                                    img_name
                                )
                                print(f"[INFO] Email sent with image: {img_name}")

                        except Exception as e:
                            print("Error checking PIR / sending email:", e)

                # Draw rectangle & label
                color = (0, 255, 0) if identity != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, identity, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    except Exception as e:
        print("Error:", e)

    cv2.imshow("Face Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()