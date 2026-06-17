import cv2
import numpy as np

# Load video stream from a file (replace with your video path)
video_path = 'car_park_7_lots.mp4'
cap = cv2.VideoCapture(video_path)

# Define horizontally aligned regions of interest (ROIs) for the parking lots
parking_lots = [
    [(30, 280), (150, 580)],   # Parking Lot 1 (leftmost)
    [(160, 280), (280, 580)],  # Parking Lot 2
    [(300, 280), (420, 580)],  # Parking Lot 3
    [(440, 280), (560, 580)],  # Parking Lot 4
    [(570, 280), (680, 580)],  # Parking Lot 5
    [(700, 280), (820, 580)],  # Parking Lot 6
    [(830, 280), (960, 580)]   # Parking Lot 7 (rightmost)
]

# Function to check if a parking lot is occupied
def is_parking_lot_occupied(roi, frame, area_threshold=2000):
    # Extract the region of interest (ROI) from the frame
    parking_spot = frame[roi[0][1]:roi[1][1], roi[0][0]:roi[1][0]]

    # Convert to grayscale and apply Gaussian blur
    gray_spot = cv2.cvtColor(parking_spot, cv2.COLOR_BGR2GRAY)
    blurred_spot = cv2.GaussianBlur(gray_spot, (5, 5), 0)

    # Adaptive thresholding
    adaptive_thresh = cv2.adaptiveThreshold(blurred_spot, 255,
                                            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY_INV, 11, 2)

    # Morphological operations to reduce noise
    kernel = np.ones((5, 5), np.uint8)
    morphed = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, kernel)

    # Find contours
    contours, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Variable to count the number of large contours found
    occupied_count = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > area_threshold:  # Adjust this value as necessary
            occupied_count += 1  # Count this as an occupied spot

    # Decide if the parking lot is occupied based on the count of large contours
    return occupied_count > 0  # More than 0 large contours indicate an occupied parking lot

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("End of video stream or error.")
        break

    # Resize the frame for consistency
    frame = cv2.resize(frame, (1024, 600))

    occupied_count = 0  # Initialize occupied count

    # Process each parking lot
    for i, roi in enumerate(parking_lots):
        occupied = is_parking_lot_occupied(roi, frame)

        # Draw rectangle around the parking spot (Green = Free, Red = Occupied)
        color = (0, 255, 0) if not occupied else (0, 0, 255)
        cv2.rectangle(frame, roi[0], roi[1], color, 2)

        # Count occupied lots
        if occupied:
            occupied_count += 1

        # Display the status on the frame
        status_text = 'Occupied' if occupied else 'Free'
        cv2.putText(frame, f"Lot {i+1}: {status_text}", (roi[0][0], roi[0][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)  # Regular size for individual lots

    # Display overall parking lot status on the top left with larger text
    if occupied_count == len(parking_lots):
        overall_status_text = "Car park full"
    else:
        available_spots = len(parking_lots) - occupied_count
        overall_status_text = f"Car park: {available_spots} available"

    # Draw the overall status text with increased size
    cv2.putText(frame, overall_status_text, (30, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 2.0, (255, 255, 255), 3)  # Increased font scale to 1.0 and thickness to 2

    # Show the video frame with annotations
    cv2.imshow('Parking Lot Detection', frame)

    # Exit if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
