# docs regarding marathos lab


### What NOT to do: Cartesian product
- I just managed to do a cartesian product even though I KNEW I could easily fall into this "trap" when it comes to dimensional modeling. Apparently there is a name for it, a `fan trap`:

```
A fan trap is a data modeling anti-pattern that occurs when joining multiple one-to-many relationships, leading to ambiguity and inflated metrics
```

What lead up to this *fan trap* is this query:
```sql

SELECT
    f.year_of_event,
    COUNT(DISTINCT e.event_id) AS total_events_hosted,
    SUM(e.event_number_of_finishers) AS total_global_finishers
FROM
    marathos.gold.fact_results f
    JOIN marathos.gold.dim_event e on f.event_id = e.event_id
    GROUP BY
        f.year_of_event
ORDER BY
    f.year_of_event ASC;
```

Reason why it happened is this:  

- Because `fact_results` contains one row per athlete, and I join it against `dim_event`, the dimension `event_number_of_finishers` will be **duplicated for each athlete who ran the race.** If a race had 100 finishers, my query will add up the number **100 a hundred times**. 
    - Resulting in *10,000 finishers*. This is a catastrophic Cartesian like explosion, usually called a `cartesian product`, or in `SQL` terms: A `cross-join`.

---

To build this mart correctly I have two ways to go, depending on how I decide to use my schema.

### 1) **Trust my fact table**
- Since the fact table actually contains all the individual achievements, I do not even need to look at the dimensions pre-aggregated total to get the number of finishers. I can just count the rows in the fact table like this:

```sql
CREATE OR REFRESH MATERIALIZED VIEW marathos.gold.mart_event_growth
  COMMENT "Year-over-year growth of events and finishers (Fact-driven)" AS
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
```
With this query i dont really *need* the `JOIN` and I can skip it entirely which will make my query super fast.
---

### 2) **Trust the Dimension modeling and go with the aggregation path**

- If I were to say that `event_number_of_finishers` is the official since some athletes could be missing from the `fact table` due to data washing in silver, then I should not involve the `fact table` at all and would group directly on my `event dimension` which would look like this:

```sql 
CREATE OR REFRESH MATERIALIZED VIEW marathos.gold.mart_event_growth
  COMMENT "Year-over-year growth of events and finishers (Dim-driven)" AS
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
```
