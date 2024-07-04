import sys
from fastkml import kml


def read_kml(kml_file):
    with open(kml_file, "r") as f:
        kml_str = f.read()
    k = kml.KML()
    k.from_string(kml_str)
    return k


def extract_coordinates(kml_data):
    coordinates = []

    for feature in kml_data.features():
        for placemark in feature.features():
            coords = placemark.geometry.coords[0]
            coordinates.append({'lng': coords[0], 'lat': coords[1]})

    return {'k1': coordinates}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python kml2jsarr.py [path_to_kml_file] [optional: html_file cs585-OL.html]")
    else:
        kml_file = sys.argv[1]
        kml_data = read_kml(kml_file)
        coords_array = extract_coordinates(kml_data)

        if len(sys.argv) == 2:
            print(coords_array)
        else:
            html_file = sys.argv[2]
            with open(html_file, 'r', encoding='utf-8') as file:
                data = file.readlines()

            data[28] = 'var d = '+str(coords_array)+'\n'

            with open(html_file, 'w', encoding='utf-8') as file:
                file.writelines(data)
