# HW3: Spatial Data

The following files are for submission:

* [X] 13 selfies, from step 1 above [if you don't submit these, you will LOSE 2 points!]
  * [ ] All in ./images/ folder with names
* [X] your .kml file from step 5 above - with the placemarks, convex hull and nearest-neighbor line segments ( **1 point** )
  * [ ] photos2kml.py - Python Script to generate KML
  * [ ] photos_convexhull_4nn.kml
* [X] a text file (.txt or .sql) with your two queries from step 5 - table creation commands (if you use Postgres and directly specify points in your queries, you won't have table creation commands, in which case you wouldn't need to worry about this part), and the queries themselves ( **2 points** )
  * [ ] spatialdbqueries.py - Python Script to take KML with points (not lines) and add to Postgres+PostGIS DB  [CHANGE DB LOGIN INFO]
  * [ ] pt5_dataloading.sql - create table and load data
  * [ ] pt5_q1.sql - Convex Hull
  * [ ] pt5_q2.sql - Top 4 Nearest Neighbors
* [X] screengrabs from steps 3,5 ( **1 point** )
  * [ ] kmlsnapshot.py - Python Script to take snapshot of specified KML file on Google Earth
  * [ ] photos_convexhull_4nn_snapshot.png
  * [ ] photos_snapshot.png
* [X] a .html file (with the OpenLayers code) from step 6, or a CodePen/jsfiddle link ( **1 point** )
  * [ ] kml2jsarr.py - Python script to edit OL.html with KML data points
  * [ ] OL.html
* [X] your Spirograph point generation code, the resulting .kml file ("spiro.kml"), shapefile (this needs to be a .zip) and a screenshot ( **1 point** )
  * [ ] spirograph.py - Python Script to generate KML
  * [ ] spirograph.kml - Spirograph KML
  * [ ] spirograph.zip - Spirograph Shapefile
  * [ ] bbalamur_spirograph.png - ArcGIS snapshot

Commands to run yourself:

* Install requirements

```bash
pip install -r requirements.txt
```

* convert directory of photos to kml

```bash
python .\photos2kml.py images photos.kml
```

* take snapshot of kml on google earth

```bash
python .\kmlsnapshot.py .\photos.kml photos_snapshot.png
```

* run SpatialDB queries with auto kml data loading and output kml with convex hull and 4 nearest neighbors

```bash
python .\spatialdbqueries.py .\photos.kml Origin_Livermore photos_convexhull_4nn.kml
```

* take snapshot of kml w/ convex hull and 4 nearest neighbors on google earth

```bash
python .\kmlsnapshot.py .\photos_convexhull_4nn.kml photos_convexhull_4nn_snapshot.png
```

* convert kml into js array for html + insert into html

```bash
python kml2jsarr.py .\photos.kml .\OL.html
```

* generate spirograph kml

```bash
python .\spirograph.py
```

* take snapshot of spirograph kml on google earth

```bash
python .\kmlsnapshot.py .\spirograph.kml spirograph_google_earth.png
```
