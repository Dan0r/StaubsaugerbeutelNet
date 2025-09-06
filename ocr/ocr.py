import cv2
import sqlite3
from easyocr import Reader
import os

# Function for processing the images. 
# image_reader will make it loop through the directory with the images. It processes the images one by one.
# reader will be for the EasyOCR object, to detect the text using its .readtext-method.

# image_directory will be loope
def get_imagetext(image_directory, reader):
    try:
        image_processed = cv2.imread(image) 
        if image_processed is None:
            raise ValueError("Image wasn't found")

        # Sort the text into columns. Sets a midpoint in the image. Then sorts x-coordinates (x-cord) with a lower value than the midpoint's x_cord as "left"; higher values as "right".
        height, width, channels = image_processed.shape
        x_midpoint = width / 2

        left_column = []
        right_column = []

        # The .readtext-method will come from EasyOCR's reader-object.'
        results = reader.readtext(image_processed, slope_ths=2, width_ths=1)

        for bbox, text, prob in results:
            x_cords = [point[0] for point in bbox]
            left_xcord = min(x_cords)

            # Store text in array
            if left_xcord <= x_midpoint:
                left_column.append((bbox, text, prob))
            else:
                right_column.append((bbox, text, prob))

        # Sort by column. To resemble the structure of the real world text.
        brand_names = []
        # We can actually detect brand names too, because they contain only uppercase ALPHABETICAL CHARACTERS.
        for column in (left_column, right_column):
            for bbox, text, prob in column:
                if text.isupper() & text.isalpha(): 
                    brand_names.append(text)

        bag_names = []
            # Detect names of vacuums
            for column in (left_column, right_column):
                for bbox, text, prob in column:
                # Avoid brand names.
                    if text not in brand_names:
                        bag_names.append(text)

                # Pop the box's headline "GEEIGNET FÜR...".
                bag_names.pop(0)

        for column in (left_column, right_column):
            for bbox, text, prob in column:
                print(text)


        print(f"Finished processing: {image}.")
    except Exception as e:
        print(f"Error processing image: {e}.")

    # Write data into an SQL-Database




# Initialise EasyOCR 
reader = Reader(['en', 'de'])

# load multiple images, that are stored in a directory called "images"
# os.walk loads top-to-bottom
image_directory = '/home/furukawa/programming/staub/ocr/images/'

for root, dirs, files in os.walk(image_directory):
    # OCR the first image, then repeat with the next
    for name in files:
        image = os.path.join(root, name)
        get_imagetext(image_directory, reader)

