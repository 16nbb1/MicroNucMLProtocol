import glob
from sys import argv
import os
from PIL import Image
from pathlib import Path

# the directory that holds the input images
path = str(argv[1])
# the file extension for the input images
ext = str(argv[2])

# the xtop-left,ytop-left and xbottom-right,ybottom-right coordinates
box = (int(argv[3]), int(argv[4]), int(argv[5]) , int(argv[6]))

# we loop through all the original files, make the Processed directory, crop the images, and save
for f in glob.glob(path + f"/**/*.{ext}", recursive=True):
	processed_dir = os.path.join(os.path.dirname(f)+"_Processed")
	os.makedirs(processed_dir, exist_ok=True)

	img_path = os.path.join(processed_dir, os.path.basename(f))
	
	with Image.open(f) as img:
		cropped_img = img.crop(box)
		cropped_img.save(img_path)
