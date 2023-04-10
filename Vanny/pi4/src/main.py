# Import the necessary libraries
import picamera
import numpy as np
import tflite_runtime.interpreter as tflite_interpreter
from io import BytesIO
import cv2

# Load the TFLite model
interpreter = tflite_interpreter.Interpreter(model_path='detect.tflite')
interpreter.allocate_tensors()

# Get the input and output details of the model
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

# Initialize the PiCamera and set its resolution
camera = picamera.PiCamera()
camera.resolution = (640, 480)

# Start the PiCamera preview
camera.start_preview()

# Initialize the stream for the PiCamera output
stream = BytesIO()

# Continuously capture frames from the PiCamera
for _ in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
    # Convert the captured image to a numpy array
    frame = np.frombuffer(stream.getvalue(), dtype=np.uint8)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    # Preprocess the image
    resized = cv2.resize(frame, (width, height))
    input_data = np.expand_dims(resized, axis=0)
    input_data = (np.float32(input_data) - 127.5) / 127.5

    # Run inference on the input image
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # Get the bounding boxes for the detected objects
    boxes = output_data[0, :, :]

    # Filter out low-confidence detections
    detections = [((int(box[1] * frame.shape[1]), int(box[0] * frame.shape[0])),
                   (int(box[3] * frame.shape[1]), int(box[2] * frame.shape[0]))) for box in boxes if box[4] > 0.6]

    # Draw the bounding boxes for the detected objects
    for detection in detections:
        box_start, box_end = detection
        cv2.rectangle(frame, box_start, box_end, (0, 255, 0), 2)

    # Display the processed frame
    cv2.imshow('Object Detection', frame)
    cv2.waitKey(1)

    # Reset the stream for the next capture
    stream.seek(0)
    stream.truncate()

# Clean up the resources
camera.stop_preview()
cv2.destroyAllWindows()