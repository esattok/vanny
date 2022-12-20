from PIL import Image 
import PIL
import os
import os.path

f = r'C:\Users\Elifnur\Desktop\baby\train_data'

for file in os.listdir(f):
    f_img = f+"/"+file
    img = Image.open(f_img)
    img = img.resize((225,225))
    img.save(f_img)