import os
import shutil
import xml.etree.ElementTree as ET

# Define the path to the folder containing the XML files
folder_path = 'Logs'

# Define a list of common 2D shapes to search for
shapes = ['circle', 'square', 'rectangle', 'triangle', 'pentagon', 'hexagon', 'apocalypse', 'shape', '2d', 'secret', 'key']

square_keyword = []
circle_keyword = []
shape_keyword = []
other_files = []
sus_files = []
secret_files = []
key_files = []

# Iterate over the XML files in the folder
log_file = os.listdir(folder_path)
for filename in log_file:
    if filename.endswith('.xml'):
        file_path = os.path.join(folder_path, filename)

        try:
            # Parse the XML file
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Iterate over the elements in the XML file
            for elem in root.iter():
                # Check if the element text contains any of the shapes
                if elem.text:
                    for shape in shapes:

                        if shape == "square" and shape in elem.text.lower():
                            print(f'Found shape: {shape} in file: {filename}')
                            square_keyword.append(filename)

                        elif shape == "circle" and shape in elem.text.lower():
                            print(f'Found shape: {shape} in file: {filename}')
                            circle_keyword.append(filename)

                        elif shape == "shape" and shape in elem.text.lower():
                            print(f'Found shape: {shape} in file: {filename}')
                            shape_keyword.append(filename)

                        elif shape == "secret" and shape in elem.text.lower():
                            print(f'Found shape: {shape} in file: {filename}')
                            secret_files.append(filename)

                        elif shape == "key" and shape in elem.text.lower():
                            print(f'Found shape: {shape} in file: {filename}')
                            key_files.append(filename)

                        elif shape in elem.text.lower():
                            print(f'Found shape: {shape} in file: {filename}')
                            other_files.append(filename)

        except ET.ParseError as e:
            print(f'Error parsing file: {filename}. Error: {e}')
            sus_files.append(filename)

square = "Square"
circle = "Circle"
shape = "Shape"
others = "Others"
sus = "Sus"
secret = "Secret"
keys = "Keys"


def make_dir_if_not_exists(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


make_dir_if_not_exists(square)
make_dir_if_not_exists(circle)
make_dir_if_not_exists(shape)
make_dir_if_not_exists(others)
make_dir_if_not_exists(sus)
make_dir_if_not_exists(secret)
make_dir_if_not_exists(keys)


def copy_files_to_new_dir(folder_name, array):
    for files in array:
        file_path = f"Logs/{files}"
        filename = os.path.basename(file_path)
        dst_path = os.path.join(folder_name, filename)
        shutil.copy2(file_path, dst_path)


copy_files_to_new_dir(square, square_keyword)
copy_files_to_new_dir(circle, circle_keyword)
copy_files_to_new_dir(shape, shape_keyword)
copy_files_to_new_dir(others, other_files)
copy_files_to_new_dir(sus, sus_files)
copy_files_to_new_dir(secret, secret_files)
copy_files_to_new_dir(keys, key_files)
