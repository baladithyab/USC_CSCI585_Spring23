Author: Baladithya Balamurugan

Prerequisites:

* fastkml
* pymongo
* requests
* random
* re
* argparse
* dotenv

Python file: insert_kml_mongo.py

Use kml formatted as the examples to load into mongodb.

CLI args

* -d, --data_type  => what type of data?
  * pop_loc: popular location. assumes kml file has only points with name (photos.kml). will generate random popularity value.
  * spiro: spirograph. assumes kml file has linestring (spirograph.kml).
  * nps: pulls data from [nps.gov](https://www.nps.gov/lib/npmap.js/4.0.0/examples/data/national-parks.geojson)
* -k, --kml  => kml path
  * not needed with nps data_type
* -f, --flush => Optional[True/False]
  * Default: True
  * Flush/create collection before inserting data
