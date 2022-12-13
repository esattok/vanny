import os
import warnings
warnings.filterwarnings('ignore')

import tensorflow as tf
from PIL import Image
from helpers import run_odt_and_draw_results
from object_detection.config import MODEL_PATH, MODEL_NAME

cwd = os.getcwd()

DETECTION_THRESHOLD = 0 # Change accordingly

# Change the test file path to your test image
INPUT_IMAGE_PATH = 'test_images/images.jpeg'

im = Image.open(INPUT_IMAGE_PATH)
im.thumbnail((512, 512), Image.ANTIALIAS)
im.save(f'{cwd}/result/input.png', 'PNG')

# Load the TFLite model
model_path = f'{MODEL_PATH}/{MODEL_NAME}'
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# Run inference and draw detection result on the local copy of the original file
detection_result_image = run_odt_and_draw_results(
    f'{cwd}/result/input.png',
    interpreter,
    threshold=DETECTION_THRESHOLD
)

# Show the detection result
img = Image.fromarray(detection_result_image)
img.save(f'{cwd}/result/ouput.png')
print('-'*100)
print('See the result folder.')