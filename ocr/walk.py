import os

directory = '/home/furukawa/programming/staub/ocr/images/'
for root, dirs, files in os.walk(directory):
    for name in files:
        directory_names = os.path.join(root, name)
        print(directory_names)
