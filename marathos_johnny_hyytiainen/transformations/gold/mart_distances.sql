USE CATALOG marathos;

USE SCHEMA gold;

-- 50 KM OR UNDER MART
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
  e.event_length <= 50.0
  AND e.event_unit = 'km';

-- OVER 50KM MART
CREATE OR REFRESH MATERIALIZED VIEW marathos.gold.mart_long_km_races
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
  e.event_length > 50.0
  AND e.event_unit = 'km';



-- 5O MILE OR UNDER MART
CREATE OR REFRESH MATERIALIZED VIEW marathos.gold.mart_short_mile_races
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
  e.event_length <= 50.0
  AND e.event_unit = 'mi';

-- OVER 50 MILE  MART
CREATE OR REFRESH MATERIALIZED VIEW marathos.gold.mart_long_mile_races
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
  e.event_length > 50.0
  AND e.event_unit = 'mi';
