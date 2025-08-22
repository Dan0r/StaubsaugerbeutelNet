# Notizen

Had to closely crop the picture for EeasyOCR to work. Shows only text using (detail=0 parameter). 

Next problem: The text is out of order. It's a bounding box issue. So I can't use `paragraph=True`.
Solution is to find the midpoint of the image and then the x-coordinate of the box and sort them to the left and to the right of the midpoint.

`width_ths` worked and fixed the problem of words that include 'City' not being merged!!

Use Python to export into SQL directly.
