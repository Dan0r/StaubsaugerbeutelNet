import cv2
import sqlite3
from easyocr import Reader

# load image and database
img = '/home/furukawa/programming/ocr/e05-2.jpg'
con = sqlite3.connect("staubsauger.db")
cursor = con.cursor()

# find midpoint of image to split columns
img = cv2.imread(img)
height, width, channels = img.shape
x_midpoint = width / 2
# Midpoint method

# initialize EasyOCR
reader = Reader(['en', 'de'])
results = reader.readtext(img, slope_ths=1, width_ths=1)

left_column = []
right_column = []
# Midpoint method 
for bbox, text, prob in results:
    # sind x-coordinate and then words left of the midpoint
     x_cords = [point[0] for point in bbox]
     left_xcord = min(x_cords)
    
    # store in array
     if left_xcord <= x_midpoint:
        left_column.append((bbox, text, prob))
     else:
        right_column.append((bbox, text, prob))

for bbox, text, prob in left_column, right_column:
    print(text)
# Identify Brand Names

# Write into an sQL Database






# Collect all box x-coordinates (left and right edges)

# if box is left of midpoint print
 # first print all of those into an array
# then print box if right of midpoint
