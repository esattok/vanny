# Import the necessary libraries
import picamera
import numpy as np
import tflite_runtime.interpreter as tflite_interpreter
from io import BytesIO
import cv2

# Set the resolution and framerate of the camera
camera = picamera.PiCamera(resolution=(640, 480), framerate=30)

# Load the TensorFlow Lite model
interpreter = tflite_interpreter.Interpreter(model_path="lite-model_efficientdet_lite0_detection_metadata_1.tflite")
interpreter.allocate_tensors()

# Get the input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Define a function to preprocess the image
def preprocess(image):
    # Convert the image to a numpy array
    image = np.asarray(image)
    # Normalize the pixel values to be between 0 and 1
    image = image / 255.0
    # Resize the image to the input shape of the model
    image = np.resize(image, (input_details[0]['shape'][1], input_details[0]['shape'][2], input_details[0]['shape'][3]))
    # Add a batch dimension to the image
    image = np.expand_dims(image, axis=0)
    # Convert the image to the input data type of the model
    image = np.array(image, dtype=input_details[0]['dtype'])
    return image

# Define a function to detect objects in the image
def detect_objects(image):
    # Preprocess the image
    image = preprocess(image)
    # Set the input tensor to the preprocessed image
    interpreter.set_tensor(input_details[0]['index'], image)
    # Run the model
    interpreter.invoke()
    # Get the output tensor
    output_data = interpreter.get_tensor(output_details[0]['index'])
    # Return the detected objects
    return output_data[0]

# Define a function to draw boxes around the detected objects
def draw_boxes(image, objects):
    # Get the dimensions of the image
    height, width, _ = image.shape
    # Loop over all detected objects
    for obj in objects:
        # Get the class id and bounding box coordinates
        class_id = int(obj[1])
        ymin, xmin, ymax, xmax = obj
        # Scale the bounding box coordinates to the image size
        xmin = int(xmin * width)
        xmax = int(xmax * width)
        ymin = int(ymin * height)
        ymax = int(ymax * height)
        # Draw the bounding box on the image
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
    # Return the image with the bounding boxes
    return image

# Start the camera preview
#camera.start_preview()

# Continuously capture images and detect objects
while True:
    # Create a BytesIO object to store the captured image
    image_stream = BytesIO()
    # Capture an image and store it in the BytesIO object
    camera.capture(image_stream, format='jpeg')
    # Convert the image data in the BytesIO object to a numpy array
    image = np.frombuffer(image_stream.getvalue(), dtype=np.uint8)
    # Decode the image as a JPEG image
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # Detect objects in the image
    objects = detect_objects(image)
    # Draw boxes around the detected objects
    print(objects)
    image_with_boxes = draw_boxes(image, objects) 
    # Show the image with the boxes
    cv2.imshow('Object Detection', image_with_boxes)
    # Wait for a key press
    cv2.waitKey(1)

# Stop the camera preview
camera.stop_preview()
