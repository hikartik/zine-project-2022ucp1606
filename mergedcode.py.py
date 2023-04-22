import cv2
import numpy as np
def colorshape():

    # Define the color ranges in HSV
    color_ranges = {
    'Red': ((0, 70, 50), (10, 255, 255)) or ((170, 70, 50), (180, 255, 255)),
    'Green': ((36, 70, 50), (70, 255, 255)),
    'Blue': ((100, 70, 50), (140, 255, 255)),
    'Yellow': ((20, 70, 50), (36, 255, 255)),
    'Orange': ((10, 70, 50), (20, 255, 255)),
    'Purple': ((140, 70, 50), (170, 255, 255)),
    'Pink': ((150, 70, 50), (180, 255, 255)) or ((0, 70, 50), (10, 255, 255))}

    # Define the minimum contour area to consider
    min_contour_area = 1000

    # Create a VideoCapture object to capture from the camera
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Blur the frame to reduce noise
        blurred = cv2.GaussianBlur(hsv, (11, 11), 0)

        # Loop over the colors
        nearest_object = None
        for color, (lower, upper) in color_ranges.items():
            # Define a mask for the color
            mask = cv2.inRange(blurred, lower, upper)

            # Find contours in the mask
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Loop over the contours
            for contour in contours:
                # Calculate the area of the contour
                area = cv2.contourArea(contour)

                # Skip small contours
                if area < min_contour_area:
                    continue

                # Calculate the shape of the contour
                perimeter = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
                num_sides = len(approx)

                # Draw a bounding box around the contour
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Calculate the center of the contour
                moments = cv2.moments(contour)
                if moments["m00"] != 0:
                    cx = int(moments["m10"] / moments["m00"])
                    cy = int(moments["m01"] / moments["m00"])
                else:
                    cx, cy = 0, 0

                # Keep track of the nearest object
                if nearest_object is None or ((cx**2 + cy**2)**0.5) < ((nearest_object[0]**2 + nearest_object[1]**2)**0.5):
                    nearest_object = (cx, cy, color, num_sides)

        # Print the shape and color of the nearest object
        if nearest_object is not None:
            cx, cy, color, num_sides = nearest_object
            shape = None
            if num_sides == 3:
                shape = 'triangle'
            elif num_sides == 4:
                shape = 'square'
            elif num_sides >= 5:
                shape = 'circle'
            color_name = color.capitalize()
            text = f'{color_name} {shape}'
            cv2.putText(frame, text, (cx - 50, cy - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            # Show the frame
            cv2.imshow('frame', frame)
            print(frame)

            # Exit the loop if the 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()

def barcode():
# Define the threshold for deciding whether a strip is white or black
    strip_threshold = 200

# Define the number of black strips needed to turn left or right
    left_threshold = 2
    right_threshold = 3

# Create a VideoCapture object to capture from the camera
    cap = cv2.VideoCapture(0)

    while True:
    # Read a frame from the camera
        ret, frame = cap.read()
        if not ret:
            break

    # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply a threshold to the grayscale image to get a binary image
        ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Split the binary image into 7 parts horizontally, each part containing one strip of the barcode
        strip_height = binary.shape[0] // 7
        strips = [binary[i:i+strip_height, :] for i in range(0, binary.shape[0], strip_height)]

    # Calculate the mean intensity of each strip and decide whether it is white or black
        is_black = [np.mean(strip) < strip_threshold for strip in strips]

    # Count the number of black strips and decide the direction of turning
        num_black = sum(is_black)
        if num_black < left_threshold:
            print("Turn left")
        elif num_black > right_threshold:
            print("Turn right")
        else:
            print("Go straight")

        # Show the frame
        cv2.imshow('frame', frame)

        # Exit the loop if the 'q' key is pressed
        if cv2.waitKey(1) == ord('q'):
            break

    # Release the VideoCapture object and close all windows
    cap.release()
    cv2.destroyAllWindows()
cap = cv2.VideoCapture(0)
colorshape()
