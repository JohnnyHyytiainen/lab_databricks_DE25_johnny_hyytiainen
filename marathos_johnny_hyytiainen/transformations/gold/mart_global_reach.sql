USE CATALOG marathos;

USE SCHEMA gold;

CREATE OR REFRESH MATERIALIZED VIEW marathos.gold.mart_global_reach
  COMMENT "Serving view - Gold layer, athlete statistics aggregated by home country" AS
SELECT
  c.iso_code,
  c.country_name,
  COUNT(f.result_id) AS total_participants,
  ROUND(AVG(f.athlete_average_speed), 2) AS national_avg_speed_kmh
FROM
  marathos.gold.fact_results f
    JOIN marathos.gold.dim_athlete a
      ON f.athlete_id = a.athlete_id
    JOIN marathos.gold.dim_country c
      ON a.athlete_country = c.iso_code
GROUP BY
  c.iso_code,
  c.country_name;