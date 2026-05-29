-- Mart för att få insights om de officiella "biljettköparna" i varje event över tid
-- Detta är baserat på min dimension, de riktiga "intäkterna" till Marathos som företag


CREATE OR REFRESH MATERIALIZED VIEW marathos.gold.mart_event_growth_official
  COMMENT "Serving view - Gold layer, year-over-year growth of events 'tickets sold' (Dim driven)" AS
SELECT
  YEAR(e.event_dates) AS year_of_event,
  COUNT(e.event_id) AS total_events_hosted,
  SUM(e.event_number_of_finishers) AS total_global_finishers
FROM
  marathos.gold.dim_event e
GROUP BY
  YEAR(e.event_dates)
ORDER BY 
  year_of_event ASC;