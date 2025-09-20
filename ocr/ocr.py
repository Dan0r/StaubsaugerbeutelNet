#!/usr/bin/env python3

import cv2
import sqlite3
from easyocr import Reader
import os
import psycopg2
from dotenv import load_dotenv

def get_imagetext(name, image, reader):
    """
    Process text from an image of the packaging.
    """

    # Define the name of the vacuum bag. For this to work the name of the image has to have the name of the vacuum bag before the "-".
    vacuumbag_name = name[:name.index("-")]

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

        # Put strings into dictionaries and clean data for headers, known outliers or even typos in the packaging text
        text_anomalies = ["JMALLFLRLR",
                          "GEEIGNET FÜR FOLGENDE MODELLE:",
                          "WEITERE MODELLE AUF DER ANDEREN SEITE"]

        data = []
        alpha = None
        for column in (left_column, right_column):
            for bbox, text, prob in column:
                # JMALLFLRLR is a known typo 
                if text.isupper() and text.isalpha() and any(text in element for element in text_anomalies) == False:
                    alpha = text
                elif any(text in element for element in text_anomalies) == False:
                    data.append({"bag": vacuumbag_name, "vacuum": text, "brand": alpha})

        return data
        # Delete the box's headline "GEEIGNET FÜR...".
        # if vacuum_names:
        #     vacuum_names.pop(0)

        print(f"Finished processing: {image}.")

        # for vacuum_name in vacuum_names:
        #     data.append({"bag": vacuumbag_name,"vacuum": vacuum_name})

    except Exception as e:
        print(f"Error processing image: {e}.")

# Write data into an SQL-Database
def post_text(vacuumbag_name, vacuum_names, brand_names, conn):
    """Get the strings from get_imagetext and post it to a SQL Database"""
    # Create Tables for data, if they don't exist yet.
    create_table_vacuums_query = """
    CREATE TABLE IF NOT EXISTS vacuums (
    id SMALLSERIAL NOT NULL PRIMARY KEY,
    vacuum_name VARCHAR(255),
    bag_name VARCHAR(255)
    );
    """

    create_table_brand_names_query = """
    CREATE TABLE IF NOT EXISTS brands (
    id SMALLSERIAL NOT NULL PRIMARY KEY,
    brand_name VARCHAR(255)
    );
    """

    insert_query_vacuums = """
    INSERT INTO vacuums (vacuum_name, bag_name) VALUES (%s, %s);
    """
    data_vacuums = (vacuum_names, vacuumbag_name)

    insert_query_brands = """
    INSERT INTO brands (brand_name) VALUES (%s);
    """
    data_brands = (brand_names)



    with conn.cursor() as cur:
        cur.execute(create_table_vacuums_query)
        cur.execute(insert_query_vacuums, data_vacuums)

        cur.execute(create_table_brand_names_query)
        cur.execute(insert_query_brands, data_brands)

    conn.commit()
    conn.close()


def main():
    """Main function"""

    # Initialise EasyOCR and Postgres
    reader = Reader(['en', 'de'])
    load_dotenv()
    
    # Open database-connection
    try:
        conn = psycopg2.connect(host="localhost", dbname="staub", user="postgres", port=5432, password=os.getenv("postgres-password"))
        print("Connected to database.")
    except:
        print("Unable to connect to the database.")

    # load multiple images, that are stored in a directory called "images"
    # os.walk loads top-to-bottom
    image_directory = '/home/furukawa/programming/staub/ocr/images/'

    for root, dirs, files in os.walk(image_directory):
        # OCR the first image, then repeat with the next
        for name in files:
            image = os.path.join(root, name)
            data = get_imagetext(name, image, reader)
    print(data)
        
        # pass data into post_text


if __name__ == "__main__":
    main()
