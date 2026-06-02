# 02_silver_layer_docs.md

## Script: `marathos_obt.py` & ERD Design `marathos_pdm.png`

### 1. Purpose (The What)

The Silver layer acts as the platforms "washing machine". The `marathos_obt.py` script builds a "One-Big-Table" (OBT) from the raw data in Bronze. Here, strict business rules are applied, regular expressions are used to extract information, and the creation of unique identifiers (Surrogate Keys) via cryptographic hashing. The ERD design then lays the foundation for how this OBT will be normalized into a Snowflake schema in the Gold layer.

---

### 2. Architectural decisions (The Why)

* **Fail Fast Principle (Data Quality):** I made an active architectural decision to discard certain rows that were corrupt rather than trying to "rescue" them. For example, performances with "d" (days) are filtered out, and unreasonable ages (negative or over 100 years) are dropped (`filter((col("age_at_event") >= 15) & (col("age_at_event") <= 100))`). This protects downstream analytics from junk data.

* **Idempotent Hashing (Surrogate Keys):** Since the raw data lacked a unique ID for each result, and `event_id` was missing entirely, I decided to use PySparks `sha2()` to create deterministic hash keys based on business logic (ex: `event_name` + `event_dates`). No matter how many times I'd run the pipeline, a race will *always* get the same ID, enabling proper JOINs in Gold.

* **Separation of Dimensions (ERD):** By looking at the ERD, one can see that the data has been deliberately separated. Instead of keeping everything in the OBT, the fact table points to four dimensions (`dim_event`, `dim_athlete`, `dim_country`, `dim_date`). This eliminates data redundancy and makes the system able scale.

---

### 3. Technical details (The How)

* **Regex Extraction:** `event_country` was dynamically extracted from `event_name` via Regex (`r"\(([^()]+)\)$"`) and the original string was cleaned up. Distance and unit were split into `event_length` (double) and `event_unit` (string)

* **Time Conversion:** The performance time ("HH:MM:SS") was split and mathematically converted to a `double` representing hours.

* **Sanity Checks & Null Handling:** The world record check `when(col("athlete_average_speed") > 25.0, lit(None))` was applied, and missing values ​​were systematically filled with `"Missing"`.

* **Deduplication:** Dropped duplicates per event, id and year to ensure the streaming pipeline remains stable.

---