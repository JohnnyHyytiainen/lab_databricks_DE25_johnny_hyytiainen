-- Använd rätt katalog och schema
USE CATALOG marathos;

USE SCHEMA gold;

-- SHORT KM MART (under 50KM)
CREATE OR REFRESH MATERIALIZED VIEW marathos.gold.mart_short_km_races
  COMMENT "Serving view - Gold layer" AS
SELECT
  f.*,
  e.event_name,
  e.event_country
FROM
  marathos.gold.fact_results f
    JOIN marathos.gold.dim_event e
      ON f.event_id = e.event_id
WHERE
  e.event_length < 50.0
  AND e.event_unit = 'km';

-- 50 KM MART
CREATE OR REFRESH MATERIALIZED VIEW marathos.gold.mart_50km_races
  COMMENT "Serving view - Gold layer" AS
SELECT
  f.*,
  e.event_name,
  e.event_country
FROM
  marathos.gold.fact_results f
    JOIN marathos.gold.dim_event e
      ON f.event_id = e.event_id
WHERE
  e.event_length = 50.0
  AND e.event_unit = 'km';

-- 100 KM MART
CREATE OR REFRESH MATERIALIZED VIEW marathos.gold.mart_100km_races
  COMMENT "Serving view - Gold layer" AS
SELECT
  f.*,
  e.event_name,
  e.event_country
FROM
  marathos.gold.fact_results f
    JOIN marathos.gold.dim_event e
      ON f.event_id = e.event_id
WHERE
  e.event_length = 100.0
  AND e.event_unit = 'km';

-- ULTRA KM MART (over 100km)
CREATE OR REFRESH MATERIALIZED VIEW marathos.gold.mart_ultra_km_races
  COMMENT "Serving view - Gold layer" AS
SELECT
  f.*,
  e.event_name,
  e.event_country
FROM
  marathos.gold.fact_results f
    JOIN marathos.gold.dim_event e
      ON f.event_id = e.event_id
WHERE
  e.event_length > 100.0
  AND e.event_unit = 'km';

-- SHORT MILE MART
CREATE OR REFRESH MATERIALIZED VIEW marathos.gold.mart_short_mi_races
  COMMENT "Serving view - Gold layer" AS
SELECT
  f.*,
  e.event_name,
  e.event_country
FROM
  marathos.gold.fact_results f
    JOIN marathos.gold.dim_event e
      ON f.event_id = e.event_id
WHERE
  e.event_length < 50.0
  AND e.event_unit = 'mi';

-- 5O MILE MART
CREATE OR REFRESH MATERIALIZED VIEW marathos.gold.mart_50mi_races
  COMMENT "Serving view - Gold layer" AS
SELECT
  f.*,
  e.event_name,
  e.event_country
FROM
  marathos.gold.fact_results f
    JOIN marathos.gold.dim_event e
      ON f.event_id = e.event_id
WHERE
  e.event_length = 50.0
  AND e.event_unit = 'mi';

-- 100 MILE MART
CREATE OR REFRESH MATERIALIZED VIEW marathos.gold.mart_100mi_races
  COMMENT "Serving view - Gold layer" AS
SELECT
  f.*,
  e.event_name,
  e.event_country
FROM
  marathos.gold.fact_results f
    JOIN marathos.gold.dim_event e
      ON f.event_id = e.event_id
WHERE
  e.event_length = 100.0
  AND e.event_unit = 'mi';

-- ULTRA MILE MART (over 100 mile)
CREATE OR REFRESH MATERIALIZED VIEW marathos.gold.mart_ultra_mi_races
  COMMENT "Serving view - Gold layer" AS
SELECT
  f.*,
  e.event_name,
  e.event_country
FROM
  marathos.gold.fact_results f
    JOIN marathos.gold.dim_event e
      ON f.event_id = e.event_id
WHERE
  e.event_length > 100.0
  AND e.event_unit = 'mi';