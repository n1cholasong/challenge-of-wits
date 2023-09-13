import os
import xml.etree.ElementTree as ET


def read_location_tag(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        locations = []
        for element in root.findall('.//location'):
            locations.append(element.text)
        return locations
    except ET.ParseError as e:
        print(f'Error parsing {xml_file}: {e}')
        return []


folder_path = f'{os.getcwd()}/Logs'
for filename in os.listdir(folder_path):
    if filename.endswith('.xml'):
        xml_file = os.path.join(folder_path, filename)
        locations = read_location_tag(xml_file)
        print(f'Locations in {filename}: {locations}')
