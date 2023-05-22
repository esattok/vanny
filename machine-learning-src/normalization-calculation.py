import os
import numpy as np
from PIL import Image

image_dir = "train_images"
pixel_values = []
for filename in os.listdir(image_dir):
    image_path = os.path.join(image_dir, filename)
    with Image.open(image_path) as image:
        pixel_values.append(np.array(image.convert("RGB")).flatten())

pixel_values = np.concatenate(pixel_values)
input_norm_mean = np.mean(pixel_values)
input_norm_std = np.std(pixel_values)

print(input_norm_mean)
print(input_norm_std)