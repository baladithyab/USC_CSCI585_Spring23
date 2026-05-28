"""Build 13 location-photo PNGs by mosaicking OpenStreetMap tiles.

For each POI in HW3's photos.kml we fetch a 3×3 grid of zoom-19 OSM
tiles centered on its lat/lng and stitch them with Pillow. Output is
a 768×768 PNG showing the real-world building footprint.

This is purely a build-time tool — runs locally on dev machine, output
gets committed/uploaded with the rest of embeds/. No API keys, all
data is open OSM."""
import math
import os
import re
import sys
import time
from io import BytesIO
from urllib.request import Request, urlopen

try:
    from PIL import Image
except ImportError:
    print("ERROR: pip install Pillow", file=sys.stderr)
    sys.exit(1)

KML_PATH = sys.argv[1] if len(sys.argv) > 1 else "embeds/data/photos.kml"
OUT_DIR  = sys.argv[2] if len(sys.argv) > 2 else "embeds/data/photos"
ZOOM = 19          # max OSM zoom — gives building-footprint detail
GRID = 3           # 3×3 = 768×768
TILE = 256
USER_AGENT = "Codeseys-CSCI585-Demo/1.0 (mailto:contact@codeseys.io)"
# Use OSM standard tile server (cyclosm has nicer footprints but rate-limits)
TILE_URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"

os.makedirs(OUT_DIR, exist_ok=True)

# Inline parser since we don't need full ElementTree for this small file
poi_pattern = re.compile(
    r'<name>([^<]+)</name>\s*<Point[^>]*>\s*<coordinates>([^<]+)</coordinates>',
    re.DOTALL
)

with open(KML_PATH, encoding='utf-8') as f:
    kml = f.read()

pois = []
for m in poi_pattern.finditer(kml):
    name = m.group(1).strip()
    coords = m.group(2).strip().split(',')
    lon, lat = float(coords[0]), float(coords[1])
    pois.append((name, lat, lon))

print(f"Found {len(pois)} POIs in {KML_PATH}")

def latlon_to_tile(lat, lon, z):
    """Slippy tile math — returns (x, y) tile coords."""
    n = 2 ** z
    x = int((lon + 180.0) / 360.0 * n)
    lat_rad = math.radians(lat)
    y = int((1.0 - math.log(math.tan(lat_rad) + 1/math.cos(lat_rad)) / math.pi) / 2.0 * n)
    return x, y

def latlon_to_pixel(lat, lon, z):
    """Returns float (px, py) within the world-tile-pixel grid."""
    n = 2 ** z
    px = (lon + 180.0) / 360.0 * n * TILE
    lat_rad = math.radians(lat)
    py = (1.0 - math.log(math.tan(lat_rad) + 1/math.cos(lat_rad)) / math.pi) / 2.0 * n * TILE
    return px, py

def fetch_tile(z, x, y):
    """One OSM tile as a PIL.Image."""
    url = TILE_URL.format(z=z, x=x, y=y)
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=15) as resp:
        return Image.open(BytesIO(resp.read())).convert('RGBA')

def build_mosaic(lat, lon, out_path):
    """Center a GRID×GRID mosaic so the POI sits in the middle pixel."""
    cx, cy = latlon_to_pixel(lat, lon, ZOOM)
    canvas = Image.new('RGBA', (GRID*TILE, GRID*TILE), (255,255,255,255))
    half = GRID // 2

    # The POI's tile coords (integer)
    cxt = int(cx // TILE)
    cyt = int(cy // TILE)

    for dy in range(-half, half+1):
        for dx in range(-half, half+1):
            tx = cxt + dx
            ty = cyt + dy
            try:
                tile = fetch_tile(ZOOM, tx, ty)
            except Exception as e:
                print(f"  tile {tx},{ty} failed: {e}", file=sys.stderr)
                continue
            canvas.paste(tile, ((dx+half)*TILE, (dy+half)*TILE))
            time.sleep(0.05)  # be nice to OSM

    # Crop a centered 768×768 viewport on the POI itself
    # Compute the POI's pixel within the canvas
    canvas_origin_px = (cxt - half) * TILE
    canvas_origin_py = (cyt - half) * TILE
    poi_canvas_x = cx - canvas_origin_px
    poi_canvas_y = cy - canvas_origin_py
    half_w = (GRID*TILE) // 2
    half_h = (GRID*TILE) // 2
    left = max(0, int(poi_canvas_x - half_w))
    top = max(0, int(poi_canvas_y - half_h))
    right = left + GRID*TILE
    bottom = top + GRID*TILE
    cropped = canvas.crop((left, top, right, bottom))

    # Mark the POI center with a subtle red circle
    from PIL import ImageDraw
    draw = ImageDraw.Draw(cropped)
    cx_local = poi_canvas_x - left
    cy_local = poi_canvas_y - top
    r = 14
    draw.ellipse([cx_local-r, cy_local-r, cx_local+r, cy_local+r], outline=(220,38,38,255), width=4)
    draw.ellipse([cx_local-3, cy_local-3, cx_local+3, cy_local+3], fill=(220,38,38,255))

    cropped.convert('RGB').save(out_path, 'JPEG', quality=82, optimize=True)
    return os.path.getsize(out_path)

for name, lat, lon in pois:
    out = os.path.join(OUT_DIR, f"{name}.jpg")
    print(f"  {name:40s} ({lat:.4f}, {lon:.4f})  →  {out}")
    try:
        size = build_mosaic(lat, lon, out)
        print(f"    ✓ {size:,} bytes")
    except Exception as e:
        print(f"    ✗ {e}", file=sys.stderr)

print(f"\nDone — {len(pois)} photos in {OUT_DIR}")
