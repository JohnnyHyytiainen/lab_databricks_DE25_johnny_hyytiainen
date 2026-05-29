-- Mart för att se vilket år som hade flest events per land
-- Mart för att se hur ett land har utvecklats över tid
USE CATALOG marathos;

USE SCHEMA gold;

CREATE OR REFRESH MATERIALIZED VIEW marathos.gold.mart_numb_events_country
  COMMENT "Serving view - Gold layer, mart for insights regarding number of events per year and country. How has a nation developed over time?" AS
SELECT
  e.event_country,
  d.year,
  COUNT(DISTINCT e.event_id) AS total_events,
  COUNT(*) AS total_finishers
FROM
  marathos.gold.fact_results f
    JOIN marathos.gold.dim_event e
      ON f.event_id = e.event_id
    JOIN marathos.gold.dim_date d
      ON e.event_dates = d.date
GROUP BY
  e.event_country,
  d.year
ORDER BY
  total_events DESC