-- Mart för att få insights om NÄR på året som är "prime time" att hosta events.
-- Spelar tid på året roll för antal events beroende per månad?
-- Har tiden på året någon korrelation med en atlets prestation?
USE CATALOG marathos;

USE SCHEMA gold;

CREATE OR REFRESH MATERIALIZED VIEW marathos.gold.mart_seasonal_events_country
  COMMENT "Serving view - Gold layer, mart for insights regarding WHEN its most popular for events to take place. Does it differ for countries depending on its geographical location OR its nation wide holidays?" AS
SELECT
  e.event_country,
  d.month,
  COUNT(DISTINCT e.event_id) AS total_events,
  COUNT(*) AS total_finishers,
  AVG(f.performance) AS avg_performance
FROM
  marathos.gold.fact_results f
    JOIN marathos.gold.dim_event e
      ON f.event_id = e.event_id
    JOIN marathos.gold.dim_date d
      ON e.event_dates = d.date
GROUP BY
  e.event_country,
  d.month
ORDER BY
  total_finishers DESC;