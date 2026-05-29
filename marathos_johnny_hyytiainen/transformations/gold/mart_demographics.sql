-- Mart för at få insights kring historisk könsfördeling.

CREATE OR REFRESH MATERIALIZED VIEW marathos.gold.mart_demographics
  COMMENT "Serving view - Gold layer, aggregated performance metrics by age, gender, and year " AS
SELECT
    f.year_of_event,
    a.athlete_gender,
    a.athlete_age_category,
    a.athlete_country,
    COUNT(DISTINCT f.athlete_id)  AS total_unique_runners,
    COUNT(f.result_id)            AS total_races_completed
FROM marathos.gold.fact_results f
JOIN marathos.gold.dim_athlete a
    ON f.athlete_id = a.athlete_id
WHERE
    a.athlete_gender IN ('M', 'F', 'X')
GROUP BY
    f.year_of_event,
    a.athlete_gender,
    a.athlete_age_category,
    a.athlete_country
ORDER BY
    f.year_of_event ASC