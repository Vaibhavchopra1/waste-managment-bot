import cv2
import numpy as np

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open webcam")
    exit()

# Define color ranges in HSV

color_ranges = {
    "red": [
        (np.array([0, 120, 70]), np.array([10, 255, 255])),     # lower red
        (np.array([170, 120, 70]), np.array([180, 255, 255]))   # upper red
    ],
    "green": [
        (np.array([36, 50, 70]), np.array([89, 255, 255]))
    ],
    "blue": [
        (np.array([90, 60, 0]), np.array([121, 255, 255]))
    ],
    "yellow": [
        (np.array([20, 80, 80]), np.array([35, 255, 255]))
    ],
    "black": [
        (np.array([0, 0, 0]), np.array([180, 255, 50]))
    ]
}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    detected_color = None

    for color_name, ranges in color_ranges.items():
        mask_total = None

        # Handle multiple ranges (e.g., red wraps around HSV)
        for lower, upper in ranges:
            mask = cv2.inRange(hsv, lower, upper)
            mask_total = mask if mask_total is None else mask_total | mask
        
        # Check if enough pixels match the color
        pixels = cv2.countNonZero(mask_total)
        if pixels > 2000:  # adjust threshold if needed
            detected_color = color_name
            cv2.putText(frame, f"Detected: {color_name.upper()}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            break

    if detected_color:
        print("Detected color:", detected_color)

    cv2.imshow("Color Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

