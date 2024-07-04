import math
import simplekml


def spirograph_points(R, r, a, center_lat, center_lon, factor):
    points = []
    n = 100
    for t in range(0, int(n * math.pi * 1000), 10):
        t = t / 1000.0
        x = ((R + r) * math.cos((r / R) * t) -
             a * math.cos((1 + r / R) * t)) * factor
        y = ((R + r) * math.sin((r / R) * t) -
             a * math.sin((1 + r / R) * t)) * factor
        lat = center_lat + y
        lon = center_lon + x
        points.append((lon, lat, 50.0))
    return points


def create_kml(points, center_lat, center_lon):
    kml = simplekml.Kml()
    kml.newpoint(name='Tommy Trojan', coords=[(center_lon, center_lat)])
    ls = kml.newlinestring(name="Spirograph Curve", coords=points)
    ls.altitudemode = simplekml.AltitudeMode.relativetoground
    kml.save("spirograph.kml")


if __name__ == "__main__":
    # Tommy Trojan coordinates
    center_lat, center_lon = 34.02065969746542, -118.28542534438766
    R, r, a = 6, 1, 8

    points = spirograph_points(R, r, a, center_lat, center_lon, 0.0001)
    create_kml(points, center_lat=center_lat, center_lon=center_lon)
    print("KML file 'spirograph.kml' has been created.")
