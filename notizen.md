# Notizen

# Python Script: Detecting packaging-text with EasyOCR
EasyOCR detects text in an image. Using details=0 the script can output only text (without bounding boxes).

Problem is: EasyOCR reads only in paragraphs. But the packaging text is column-wise. The script should thus read the first column and then the second column, for the output to resemble the real structure.
Can be fixed with kind of a hack lol: 
1. Use CV2 (library) to find the middle of the picture
2. Define a point at the middle
3. Let EasyOCR read out the x_coordinates of the bounding boxes of the detected text
4. Pick x_coordinate furthes to the left.
5. If this x-coordinate is to the left of the midpoint still, the string belongs to the left column

Limitation is of course that you have to crop the pictures that you put in cleanly. But this hack works amazingly consistent.

Next step is to detect brand names. I tried to detect them by ASCII-Value using ord(c), since they are all uppercase and non-numerical. But I had some weird for-loops. The builtins .isupper() combined with .isalpha() seemed the simple solution.

# Python Script: Insert data into Postgres Database
Writing a Python script, to detect packaging text with EasyOCR.

```
CREATE TABLE staubsaugerbeutel;
bag_size
brand


CREATE TABLE staubsauger
modell
brand
bag_size
```
