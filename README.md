# USC CSCI 585 — Database Systems (Spring 2023)

My homework + project work from Yan Liu's CSCI 585 at USC.

> **Repo history note:** the original `HWs/HW4/.env` and `HWs/HW3/spatialdbqueries.py` contained live credentials for a personal MongoDB Atlas cluster and a Supabase Postgres instance. Both were rotated and the strings scrubbed from git history via `git filter-repo` on **2026-05-28** before the repo was made public. The current `.env.example` and env-driven Python code show how to point the demos at your own DB. See the audit notes inside `HWs/HW3/spatialdbqueries.py`.

## Live demos

The `embeds/` directory holds two interactive visualizations:

- **Bay Area Photo Spatial Queries** (HW3) — 13 geotagged photos, convex hull, k-NN, KDE. Same logic as the original PostGIS code, but computed in-browser with turf.js so no DB is needed.
- **YouTube SQL Schema** (HW2) — the 7-table relational schema running on **real PostgreSQL** via [PGlite](https://github.com/electric-sql/pglite). All 6 HW2 query exercises are pre-loaded.

These are rendered on [codeseys.io/projects/csci-585](https://codeseys.io/projects/csci-585) — the demo URLs are versioned per git-sha so old commits stay reachable.

## Layout

| Path | What |
|---|---|
| `HWs/HW1/` | Conceptual modeling (ER → relational) |
| `HWs/HW2/` | YouTube schema + SQL queries (q1.sql … q6.sql) |
| `HWs/HW3/` | KML + PostGIS spatial queries |
| `HWs/HW4/` | MongoDB Atlas + KML loader (env-driven; see `.env.example`) |
| `HWs/HW5/` | Image classification (chihuahua-vs-muffin etc.) |
| `Lectures/` | Annotated lecture notes |
| `Exams/` | Midterm + final review notes |
| `embeds/` | Interactive web demos (rendered on codeseys.io) |
| `web.codeseys.json` | Embed manifest (consumed by personal-site discovery) |

