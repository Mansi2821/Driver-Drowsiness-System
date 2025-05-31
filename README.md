# Driver Drowsiness Detection System

This project is a real-time driver drowsiness detection system that uses computer vision to monitor a driver's eye aspect ratio (EAR) and lip movement to detect signs of sleepiness or yawning. It alerts the driver using sound alarms when drowsiness is detected.

## 🔧 Features

- Real-time video stream from webcam
- Eye aspect ratio (EAR) analysis for drowsiness detection
- Lip movement analysis for yawn detection
- Sound alerts for both drowsiness and yawning
- Live plotting of EAR values alongside video stream

## 📁 Project Structure

- `shape_predictor_68_face_landmarks.dat`: Pre-trained dlib model for facial landmark detection (required).
- `example_WAV_1MG.wav`, `mixkit-classic-alarm-995.wav`: Sound files used for alerts.
- Python script (`.py`): Main application file (uploaded).

## 🛠️ Requirements

- Python 3.x
- Required Libraries:
  ```bash
  pip install opencv-python dlib imutils pygame matplotlib numpy scipy
🚀 How to Run
Place the facial landmark model (shape_predictor_68_face_landmarks.dat) in the same directory.

Make sure the alert sound files are present at the correct path or update the path in the code.

Run the script:

bash
Copy
Edit
python filename.py
Use --webcam argument to select a different webcam:

bash
Copy
Edit
python filename.py --webcam 1
Press q to quit the application.

📊 How It Works
Eye Detection: Calculates the EAR by measuring distances between eye landmarks.

Yawn Detection: Measures the vertical distance between top and bottom lips.

Alarms: If EAR falls below 0.3 for 30 consecutive frames, an alarm is triggered. If mouth opens widely (yawn threshold), another alarm sounds.

📸 Visualization
The application displays a side-by-side view of the webcam stream and a live graph showing the trend of EAR values over time.

👤 Author
Mansi Bhardwaj
