DROP TABLE locations;

CREATE TABLE IF NOT EXISTS locations (
            id SERIAL PRIMARY KEY,
            name VARCHAR,
            geom GEOMETRY
        );

INSERT INTO locations (name, geom)
VALUES (CCC1_Ohlone_Newark, ST_MakePoint(-122.0038279, 37.51807089972222));


INSERT INTO locations (name, geom)
VALUES (CCC2_Ohlone_Fremont, ST_MakePoint(-121.91260732777778, 37.528407219444446));


INSERT INTO locations (name, geom)
VALUES (GasStation1_Valero_Fremont, ST_MakePoint(-121.9885955, 37.547944199999996));


INSERT INTO locations (name, geom)
VALUES (GasStation2_Arco_Livermore, ST_MakePoint(-121.72327423094444, 37.71144104002778));


INSERT INTO locations (name, geom)
VALUES (Origin_Livermore, ST_MakePoint(-121.711, 37.727));


INSERT INTO locations (name, geom)
VALUES (Mall1_NewPark_Newark, ST_MakePoint(-121.99994449972222, 37.527973599999996));


INSERT INTO locations (name, geom)
VALUES (Mall2_SFPremiumOutlets_Livermore, ST_MakePoint(-121.84037929972222, 37.69927129972222));


INSERT INTO locations (name, geom)
VALUES (NaturePark1_LakeElizabeth_Fremont, ST_MakePoint(-121.96317271944444, 37.54530391944444));


INSERT INTO locations (name, geom)
VALUES (NaturePark2_PondPark_Newark, ST_MakePoint(-122.04985429999999, 37.5246865));


INSERT INTO locations (name, geom)
VALUES (Restaurant1_HotPot_Newark, ST_MakePoint(-122.01785259972222, 37.53787859972222));


INSERT INTO locations (name, geom)
VALUES (Restaurant2_TacoBell_Newark, ST_MakePoint(-122.0267891, 37.5408052));


INSERT INTO locations (name, geom)
VALUES (Theater1_Century_Fremont, ST_MakePoint(-121.97040529972223, 37.50048329972222));


INSERT INTO locations (name, geom)
VALUES (Theater2_Century_UnionCity, ST_MakePoint(-122.06788269972222, 37.5997806));