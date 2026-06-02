# 03_gold_layer_dims_facts_docs.md

## Script: Dimensions (`dim_athlete.py`, `dim_event.py`, `dim_country.py`, `dim_date.py`)

### 1. Purpose (The What)

These scripts break the broad Silver OBT into separate, specialized dimension tables. In addition, two enrichment dimensions (bonus data) are created: `dim_country` for ISO mapping and `dim_date` for calendar/seasonal analysis. This builds the descriptive part of my Snowflake architecture.

--- 

### 2. Architectural decisions (The Why)

* **Normalization (Snowflake/Star Schema):** By separating `athlete` and `event` information, I removed massive redundancy. Instead of storing the text "United States" 1.3 million times in an OBT, I chose to store it once in the dimension and reference it via an ID. This reduces storage costs and speeds up BI tools tremendously - The `serving-layer` should not do any heavy lifting and be optimized for speed.

* **Master Data Management (`dim_country`):** Bringing in an external file (`dim_countries.csv`) to map old IOC codes to modern ISO-3166 is apparently a classic Data Engineering decision. Instead of hardcoding hundreds of `REPLACE()` rules in the backend or frontend (Plotly), the "Single Source of Truth" is maintained in a manageable dimension table.

* **Pre calculated Business Logic (`dim_date`):** Generating a date dimension from 1798 to 2100 moves calculation logic (like `is_weekend` or `day_of_week`) out of the reports and down to the database. Analysts and Databricks Genies never need to write complex date arithmetic, they can just join and filter on `is_weekend = True`.

--- 

### 3. Technical details (The How)

* **Standard dimensions:** `dim_athlete` and `dim_event` are created by isolating specific columns from the OBT and applying `.dropDuplicates()` to their respective primary keys (`athlete_id` and `event_id`).

* **Dynamic Date Generation:** `dim_date` uses Sparks SQL function `sequence()` and `explode()` to rapidly generate one row per day over 300 years, then apply Boolean flags (such as weekend/weekday) based on the weekday index.

---

## Script: Fact table (`fact_results.py`)

### 1. Purpose (The What)

The script creates the absolute core of the system: The granular fact table `fact_results`. This table ties together all dimensions and stores only metrics and foreign keys for each individual result an athlete has achieved in a race.

### 2. Architectural Decisions (The Why)

* **Slim and Deep Design:** The fact table is designed to be "slim". By excluding all text and storing only the IDs and Double/Float values ​​(`performance`, `athlete_average_speed`) the I/O load (read speed from disk) is minimized. It is this design that allows the pipeline to quickly aggregate millions of rows.

* **Scalability:** Because the table does not contain any descriptive information, it will grow linearly and predictably in size for each new marathon imported through the pipeline, without degrading performance.

### 3. Technical details (The How)

* The table is built by only selecting keys (`result_id`, `event_id`, `athlete_id`) and measurable results (`performance`, `athlete_average_speed`, `year_of_event`) from `marathos_obt`.

---