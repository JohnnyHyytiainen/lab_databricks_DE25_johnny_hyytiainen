# 06_eda_bronze_silver_docs.md

## Script: `01_eda_bronze.ipynb` & `02_eda_silver.ipynb`

### 1. Purpose (The What)

These two notebooks act as the platforms "before and after" inspection: 

- `01_eda_bronze.ipynb` explores the raw data (7.46 million rows) to identify anomalies, dirty data, and inconsistent formats.

- `02_eda_silver.ipynb` then validates that the Silver layers OBT (One-Big-Table) has indeed applied all the data cleaning rules and reduced the dataset to 6.8 million high-quality rows.

---

### 2. Architectural decisions (The Why)

* **Data Profiling before coding:** By exploring the Bronze layer first, data driven decisions were made for the Silver layer logic. The discovery of performances expressed in days ("d") and negative ages guided the "Fail Fast" architectural decision to filter out invalid rows entirely, rather than building complex (and potentially incorrect) guesswork logic.

* **Validation of Pipeline Integrity:** The Silver EDA proves that the transformations worked. By plotting age distribution and speeds, it is verified that `age_at_event` is now within reasonable limits (15-100 years) and that the maximum speed is capped at 25 km/h.

---

### 3. Technical Details (The How)

* Uses `px.bar()` and `px.histogram()` for quick visual profiling of the data.

* Perform `.count()`, `.describe()` and `.display()` on Spark DataFrames to compare volumes (drop-off rate) between Bronze and Silver.

* Verifies that the SHA2 cryptographic keys (`result_id`, `event_id`) have actually been generated correctly and do not contain null values. 

* Confirmed that no null `result_ids` exist, which would indicate a failed hash on a null composite key.
