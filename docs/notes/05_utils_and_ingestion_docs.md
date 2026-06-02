# 05_utils_and_ingestion_docs.md

## Script: `schema_helpers.py`  
### 1. Purpose (The What)

This is a utility module that contains the function `rename_columns_to_snake_case()`. It takes a PySpark DataFrame, scans all column names, and recasts them to a strict `snake_case` standard, no matter how messy the original names were.

---
### 2. Architectural decisions (The Why)

* **Modularity & DRY (Don't Repeat Yourself):** Instead of cluttering up the Bronze script with 20 lines of column renames, the logic is extracted to a separate file. This keeps the main code clean and makes the functionality reusable for future data sources.

* **Defensive Programming:** External data is notoriously unpredictable. CSV files can come with spaces, special characters, or CamelCase in their headers. By enforcing a default (snake_case) *before* the data is saved to the bronze layer, I protect the entire downstream pipeline from crashing due to a misspelled column name.

---
### 3. Technical details (The How)

* The script iterates over `df.columns` and uses the Python library `re` (Regex) to find problems.

* It replaces special characters and spaces with underscores (`_`), puts underscores between lowercase and uppercase letters (to break CamelCase), and finally converts the entire string to lowercase using `.casefold()` for unicode-safe normalization before applying PySparks `withColumnRenamed`


## Script: `llm_marathon_ingest.py` (Bonus Task)

### 1. Purpose (The What)

This script acts as a synthetic data producer to test our Medallion pipeline's "Auto Loader" functionality. The script injects 50 LLM-generated, realistic rows of data for a fictional race ("Stockholm Marathos Ultra") directly into our Unity Catalog Volume.

---

### 2. Architectural decisions (The Why)

* **End-to-End Streaming Testing:** To prove that the Bronze layers Auto Loader (`cloudFiles`) is indeed picking up *new* data incrementally (without rereading 7.4 million historical rows), I needed a trigger. By dumping a new, synthetic CSV file into the `/raw/` volume, I could force the pipeline to act on new data.

* **LLM Generated Data:** LLM (Gemini) was used to generate a realistic dataset (correct age categories, realistic velocities, etc). The pipeline is deterministic, it only processes what lands in the volume.

---

### 3. Technical details (The How)

* The script contains a hardcoded CSV string with 50 LLM-generated rows that match the messy original schema (including "h" at the end of times and non-standard headers).

* Uses standard Python I/O (`open(OUTPUT_PATH, "w")`) to write the file to `/Volumes/marathos/default/raw/` directly from a Databricks script.

* Ends with a `LIST` command via Spark SQL to verify that the file successfully landed on the volume.

