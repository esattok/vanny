import os

cwd = os.getcwd()

if not os.path.exists('model'):
    os.mkdir('model')

if not os.path.exists(f'{cwd}/result'):
    os.mkdir(f'{cwd}/result')

TRAIN_DATASET_PATH = f'{cwd}/object_detection/dataset/train'
VALID_DATASET_PATH = f'{cwd}/object_detection/dataset/valid'
TEST_DATASET_PATH = f'{cwd}/object_detection/dataset/test'
MODEL_PATH = f'{cwd}/object_detection/model'

MODEL = 'efficientdet_lite0'
MODEL_NAME = 'baby.tflite'
CLASSES = ['baby']
EPOCHS = 20
BATCH_SIZE = 4