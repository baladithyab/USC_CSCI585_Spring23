import sys
from fastkml import kml
import psycopg2
import simplekml


def read_kml(kml_file):
    with open(kml_file, "r") as f:
        kml_str = f.read()
    k = kml.KML()
    k.from_string(kml_str)
    return k


def insert_coordinates_to_db(kml_data, db_config):
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("""
        DROP TABLE locations;
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id SERIAL PRIMARY KEY,
            name VARCHAR,
            geom GEOMETRY
        );
    """)

    for feature in kml_data.features():
        for placemark in feature.features():
            name = placemark.name
            coords = placemark.geometry.coords[0]
            cursor.execute(
                """
                INSERT INTO locations (name, geom)
                VALUES (%s, ST_MakePoint(%s, %s));
                """,
                (name, coords[0], coords[1])
            )

    conn.commit()
    cursor.close()
    conn.close()


def compute_convex_hull(db_config):
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ST_AsText(ST_ConvexHull(ST_Collect(geom)))
        FROM locations;
    """)

    result = cursor.fetchone()
    cursor.close()
    conn.close()

    return result[0]


def find_four_nearest_neighbors(home_name, db_config):
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT l2.name, ST_Distance(l1.geom, l2.geom) AS distance
        FROM locations l1, locations l2
        WHERE l1.name = %s AND l1.id <> l2.id
        ORDER BY distance
        LIMIT 4;
    """, (home_name,))

    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return result


def create_new_kml(kml_data, convex_hull, nearest_neighbors, home_name, filename='photos_convexhull_4nn.kml'):
    new_kml = simplekml.Kml()

    # Add original placemarks
    for feature in kml_data.features():
        for placemark in feature.features():
            new_kml.newpoint(name=placemark.name, coords=[
                             placemark.geometry.coords[0]])

    # Add convex hull polygon
    coords = [(float(coords.split(" ")[0]), float(coords.split(" ")[1]))
              for coords in convex_hull[9:-2].split(',')]
    pol = new_kml.newpolygon(name="Convex Hull", outerboundaryis=coords)

    pol.style.linestyle.color = simplekml.Color.red
    pol.style.linestyle.width = 5
    pol.style.polystyle.color = simplekml.Color.changealphaint(
        85, simplekml.Color.black)

    # Add nearest neighbor line segments
    home_coords = None
    for feature in kml_data.features():
        for placemark in feature.features():
            if placemark.name == home_name:
                home_coords = placemark.geometry.coords[0]
                break

    if home_coords:
        for neighbor in nearest_neighbors:
            neighbor_name = neighbor[0]
            neighbor_coords = None

            for feature in kml_data.features():
                for placemark in feature.features():
                    if placemark.name == neighbor_name:
                        neighbor_coords = placemark.geometry.coords[0]
                        break

            if neighbor_coords:
                ls = new_kml.newlinestring(name=f"Line({home_name},{neighbor_name})", coords=[
                    home_coords, neighbor_coords])
                ls.style.linestyle.color = simplekml.Color.gold
                ls.style.linestyle.width = 5

    new_kml.save(filename)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Usage: python spatialdbqueries.py [path_to_kml_file] [home_location_name] [new_kml_file_name]")
    else:
        kml_file = sys.argv[1]
        home_name = sys.argv[2]
        new_kml_file_name = sys.argv[3]

        # Read KML file
        kml_data = read_kml(kml_file)

        # Database configuration
        db_config = {
            'dbname': 'postgres',                          # CHANGE THIS
            'user': 'postgres',                            # CHANGE THIS
            'password': '***REVOKED***',                # CHANGE THIS
            'host': '***REVOKED-SUPABASE-HOST***',  # CHANGE THIS
            'port': '5432',
        }

        # Insert coordinates into the database
        insert_coordinates_to_db(kml_data, db_config)

        # Compute the convex hull
        convex_hull = compute_convex_hull(db_config)
        print(f"Convex Hull: {convex_hull}\n")

        # Find the four nearest neighbors
        nearest_neighbors = find_four_nearest_neighbors(home_name, db_config)
        print("Four Nearest Neighbors:")
        for neighbor in nearest_neighbors:
            print(f"Location: {neighbor[0]} - Distance: {neighbor[1]}")

        # Create new KML file
        create_new_kml(kml_data, convex_hull, nearest_neighbors,
                       home_name, new_kml_file_name)
        print("New KML file '%s' has been created." % (new_kml_file_name))
