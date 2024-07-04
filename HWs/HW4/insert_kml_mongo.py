import os
import random
import re
from fastkml import kml
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import argparse
import requests
from dotenv import load_dotenv

load_dotenv()

# Function to parse KML file and return a list of placemarks


def parse_kml_file(file_path):
    with open(file_path, "r") as kml_file:
        kml_content = kml_file.read()

    kml_content = re.sub(r'<\?xml[^>]*\?>', '', kml_content)
    kml_obj = kml.KML()
    kml_obj.from_string(kml_content)

    placemarks = []
    for feature in kml_obj.features():
        for placemark in feature.features():
            placemarks.append(placemark)

    return placemarks

# Function to generate a random popularity value between 0 and 100


def generate_random_popularity():
    return random.randint(0, 100)


# Function to create collection if not exists else empty it
def create_delete(db, collection_name):
    # Check if the collection exists
    if collection_name in db.list_collection_names():
        # If the collection exists, empty it
        db[collection_name].delete_many({})
    else:
        # If the collection does not exist, create it
        db.create_collection(collection_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Load GeoJSON data and insert into MongoDB")
    parser.add_argument(
        '-d',
        '--data_type',
        action='store',
        help="What data?\npop_loc: popular location. assumes kml file has only points with name. will generate random popularity value.",
        required=True,
        choices=['pop_loc', 'spiro', 'nps']
    )
    parser.add_argument(
        '-k',
        '--kml',
        action='store',
        help="Specify kml file path",
        default=None
    )
    parser.add_argument(
        '-f',
        '--flush',
        action='store_true',
        help="Flush the collection before inserting data",
        default=True
    )
    args = parser.parse_args()

    q = args.data_type
    if args.kml:
        placemarks = parse_kml_file(args.kml)
    flush = args.flush

    uri = os.environ['MONGODB_CONNECTION_URI']
    # Create a new client and connect to the server
    mongo_client = MongoClient(uri, server_api=ServerApi('1'))
    db = mongo_client['HW4DB']

    # Insert placemarks data into MongoDB

    batch_data = []
    collection = None

    if q == 'pop_loc':
        collection_name = 'HW3Data'
        if flush:
            create_delete(
                db=db,
                collection_name=collection_name
            )
        collection = db[collection_name]
        for placemark in placemarks:
            data = {
                "name": placemark.name,
                "popularity": generate_random_popularity(),
                "loc": [placemark.geometry.x, placemark.geometry.y],
            }
            batch_data.append(data)

    elif q == 'spiro':
        collection_name = 'Spiro'
        if flush:
            create_delete(
                db=db,
                collection_name=collection_name
            )
        collection = db[collection_name]
        for placemark in placemarks:
            if placemark.geometry.geom_type == "Point":
                data = {
                    "loc": [placemark.geometry.x, placemark.geometry.y]
                }
                batch_data.append(data)
            elif placemark.geometry.geom_type == "LineString":
                for coord in placemark.geometry.coords:
                    data = {
                        "loc": [coord[0], coord[1]]
                    }
                    batch_data.append(data)

    elif q == 'nps':
        collection_name = 'NPS'
        if flush:
            create_delete(
                db=db,
                collection_name=collection_name
            )
        collection = db[collection_name]
        url = "https://www.nps.gov/lib/npmap.js/4.0.0/examples/data/national-parks.geojson"
        response = requests.get(url)
        geojson_data = response.json()

        # Extract features and prepare documents for MongoDB
        batch_data = geojson_data["features"]

    collection.insert_many(batch_data)

    print("Data has been successfully imported into MongoDB.")
