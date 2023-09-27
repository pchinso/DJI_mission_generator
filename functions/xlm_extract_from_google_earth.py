import xml.etree.ElementTree as ET
import json

def extract_coordinates(xml_file_path):
    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Define a list to store the extracted coordinates
    coordinates_list = []
    points_list = []

    # Find all <coordinates> elements in the XML
    for coordinates_element in root.findall(".//{http://www.opengis.net/kml/2.2}coordinates"):
        # Split the text inside <coordinates> element by commas and extract x, y, z values
        coordinates_text = coordinates_element.text.strip()
        coordinates = coordinates_text.split(',')
        if len(coordinates) == 3:
            x, y, z = map(float, coordinates)
            coordinates_dict = {'long': x, 'lat': y, 'elev': z}
            coordinates_list.append(coordinates_dict)

    # Find all <coordinates> elements in the XML
    for point_element in root.findall(".//{http://www.opengis.net/kml/2.2}name"):
        # Split the text inside <coordinates> element by commas and extract x, y, z values
        point_text = point_element.text.strip()
        points_dict = {'Point_name': point_text}
        points_list.append(points_dict)
    
    if len(points_list) > len(coordinates_list):
       points_list.pop(0)
       merged_list = [dict1.update(dict2) or dict1 for dict1, dict2 in zip(points_list, coordinates_list)]

    return merged_list


# Example usage
xml_file_path = '/home/pcs/Documents/Python/DJI_mission_generator/sample_klm_dji_pilot/ST8_mission_google_earth.kml'
coordinates = extract_coordinates(xml_file_path)

# print(coordinates)


with open("coordinates.json", "w") as outfile:
  json.dump(coordinates, outfile, indent=4)
  # Export to JSON with pretty format using dumps()
  json_data = json.dumps(coordinates)
