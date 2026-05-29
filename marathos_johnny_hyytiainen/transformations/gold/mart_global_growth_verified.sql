-- Mart för att få insights om de officiella deltagarna i varje event över tid
-- Detta är baserat på min FACT table, de riktiga deltagarna som tog sig över mållinjen under Marathos event

CREATE OR REFRESH MATERIALIZED VIEW marathos.gold.mart_event_growth_verified
  COMMENT "Serving view - Gold layer, year over year growth of events and finishers (Fact table)" AS
SELECT
  year_of_event,
  COUNT(DISTINCT event_id) AS total_events_hosted,
  COUNT(result_id) AS total_global_finishers
FROM
  marathos.gold.fact_results
GROUP BY
  year_of_event
ORDER BY 
  year_of_event ASC;
