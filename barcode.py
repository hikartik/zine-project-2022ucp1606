import cv2
import numpy as np

# Define barcode width and bit width
BARCODE_WIDTH = 100
BIT_WIDTH = 10

# Create a QRCodeDetector object
qr_decoder = cv2.QRCodeDetector()

# Read barcode image from file or camera
# Use '0' for default camera
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        continue
    
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Threshold image to black and white
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Find barcode by detecting four consecutive white strips
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    barcode = None
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w == BARCODE_WIDTH and h > BIT_WIDTH * 3:
            # Check if the barcode consists of four consecutive white strips
            bits = [1 if binary[y:y+h, x+i*BIT_WIDTH:x+(i+1)*BIT_WIDTH].mean() > 127 else 0 for i in range(4)]
            if bits == [0, 1, 0, 1]:
                barcode = binary[y:y+h, x:x+w]
                break
    
    if barcode is not None:
        # Decode barcode using cv2.QRCodeDetector()
        data, _, _ = qr_decoder.detectAndDecode(barcode)
        if len(data) > 0:
            # Get the direction from the decoded data
            direction = int(data)
            print(f"Turn {direction} degrees")
            # Uncomment the following line to draw a rectangle around the barcode
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Show the original frame and barcode detection
    cv2.imshow('Frame', frame)
    if barcode is not None:
        cv2.imshow('Barcode', barcode)
    
    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
