import os
import sys
from GPSPhoto import gpsphoto
from simplekml import Kml


def get_photo_coordinates(photo_path):
    try:
        photo = gpsphoto.GPSPhoto(photo_path)
        gps_info = photo.getGPSData()
        return gps_info['Latitude'], gps_info['Longitude']
    except Exception as e:
        print(f"Error: {e}")
        return None


def create_kml_from_photos(directory, kml_file_name):
    kml = Kml()

    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                file_path = os.path.join(root, file)
                coords = get_photo_coordinates(file_path)
                if coords:
                    lat, lon = coords
                    kml.newpoint(name=file.split('.')[0], coords=[(lon, lat)])

    kml.save(kml_file_name)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python photos_to_kml.py [path_to_photos_directory] [kml_file_name]")
    else:
        directory = sys.argv[1]
        kml_file_name = sys.argv[2]
        create_kml_from_photos(directory, kml_file_name)
        print("KML file '%s' has been created." % (kml_file_name))
