# 07_gold_validation_and_testing_docs.md

## Script: `03_eda_gold.ipynb`, `05_genie_testing.ipynb` & `06_llm_testing_marathon.ipynb`

### 1. Purpose (The What)

These notebooks constitute the final Quality Assurance (QA) of the system:
- `03_eda_gold.ipynb` validates the dimensional model (Snowflake schema) and Marts.

- `05_genie_testing.ipynb` documents the outcome of the AI ​​assistants SQL generation. 

- `06_llm_testing_marathon.ipynb` analyzes the injection of synthetic LLM data and how this affected the integrity of the pipeline.

---

### 2. Architectural decisions (The Why)

* **LLM Ingestion & Data Corruption (The Fail Fast Test):** When injecting synthetic data via `llm_marathon_ingest.py`, a scenario arose where the LLM generated data that violated the schema (e.g. incorrect headers or data types). This temporarily corrupted the load into Silver. This was an unintended but great stress test! It proved *why* strict Schema Enforcement and helpers (`schema_helpers.py`) are absolutely necessary in production environments to protect the system from hallucinated source data.


* **Semantic Model Control (Genie):** Testing of Databricks Genie revealed that the AI ​​preferred to read from dimensions instead of fact tables (resulting in small differences, example: 7705 vs 7717 unique events) The insight here was that an LLM requires explicit configuration of "Measures" and "Filters" to understand business logic (Official vs. Verified).

---

### 3. Technical Details (The How)

* Verify that the synthetic athlete with `athlete_id` = 2000000 from "Stockholm Marathos Ultra" actually flowed all the way from the raw CSV to the Gold fact table.

* Documents 11 unique test prompts against Genie and analyzes the sources of error where Genies SQL code was chosen to go against `dim_event` instead of `fact_results`.

