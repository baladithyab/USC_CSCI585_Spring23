SELECT l2.name, ST_Distance(l1.geom, l2.geom) AS distance
        FROM locations l1, locations l2
        WHERE l1.name = %s AND l1.id <> l2.id
        ORDER BY distance
        LIMIT 4;