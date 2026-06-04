# 04_gold_layer_marts_docs.md

## Script: Gold Data Marts (`mart_*.sql`)

### 1. Purpose (The What)

These SQL scripts create *Materialized Views* (Marts) on top of my Snowflake schema. They act as the platforms "checkout", where complex JOINs and heavy aggregations (SUM, COUNT, AVG) are already pre-calculated. This feeds the (`serving layer`) Databricks dashboard, Plotly scripts, and Marathos Genie with data fast.

---

### 2. Architectural decisions (The Why)

* **The solution to "The Fan Trap" (Data Quality):** The most important decision in this layer was to deliberately separate the growth calculations into two different Marts.

* `mart_event_growth_official` groups only on the Dimension (`dim_event`) to get official "tickets sold", which prevents the explosive duplication [Fan Trap](fan_trap.md) that occurs when summing a pre-aggregated number over a million-row fact table.

* `mart_event_growth_verified` instead counts actual, unique results in the Fact Table (`COUNT(result_id)`) to get the number of athletes who *actually crossed the finish line*. This gave me my "No-Show Rate" which is seen as a KPI in my dashboard with 8.6%

* **Materialized Views:** By defining the views as `CREATE OR REFRESH MATERIALIZED VIEW`, the data is pre calculated. When the business side loads its Dashboard of over 7 million performances, Databricks actually scans only a few rows in the materialized view.

* **Geographic and Temporal Separation:** By creating specialized views for seasons (`mart_seasonal_events_country`) and global reach (`mart_global_reach`), I minimize the risk of the end user(Me or `Marathos Genie`) building incorrect aggregations.

---

### 3. Technical details (The How)

* **Global Reach (`mart_global_reach.sql`):** Joins the Fact Table with both `dim_athlete` and `dim_country` to expose the `iso_3166` column. This was crucial for the Plotly/Databricks Map widgets to render Choropleth maps correctly without frontend patches.

* **Demographics (`mart_demographics.sql`):** Counts `COUNT(DISTINCT f.athlete_id)` versus `COUNT(f.result_id)`. This technical nuance allowed me to distinguish between the number of *unique runners* and the total number of *completed races* by age category and gender.

* **Seasons (`mart_seasonal_events_country.sql`):** Leverages my  `dim_date`-table to extract `month` and find correlations between time of year and average performance (`AVG(f.performance)`) by country.

---