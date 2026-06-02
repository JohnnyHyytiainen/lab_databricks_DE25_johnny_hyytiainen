# 01_bronze_layer_docs.md

## Script: `setup_unity_catalog.sql`

### 1. Purpose (The What)

This script lays the foundation for the entire project infrastructure in Databricks. It creates the logical division in the Unity Catalog by defining the `marathos` directory, its three schemas (`bronze`, `silver`, `gold`), and a `Volume` (`default.raw`) for file loading.

### 2. Architectural decisions (The Why)

* **Separation of Concerns:** By explicitly creating separate schemas (`bronze`, `silver`, `gold`), I built the Medallion architecture directly into the platform structure. This prevents analysts from accidentally reading unfiltered raw data, and ensures that different teams (example: Data Engineers vs. Data Analysts) can work in isolation.

* **Idempotency:** The use of `CREATE CATALOG IF NOT EXISTS` and `CREATE SCHEMA IF NOT EXISTS` means that the script is *idempotent*. It can be run a hundred times without crashing the environment. This is standard for Infrastructure as Code (IaC) and CI/CD pipelines.

* **Volumes for Data Lake functionality:** Creating a Unity Catalog Volume (`raw`) gives me a safe and manageable "landing zone" for raw CSV/JSON files before they are sucked into the bronze layer.

---

## Script: `raw_marathos.py`

### 1. Purpose (The What)

This is the systems "ingestion layer". The script sets up Delta Live Tables (DLT) streaming table (`raw_marathon_data`) that monitors the Volume and automatically loads any new raw data from CSV files into the bronze layer.

### 2. Architectural decisions (The Why)

* **Auto Loader (cloudFiles):** Instead of using a static `spark.read`, Databricks Auto Loader (`format("cloudFiles")`) was chosen. This is a critical decision because Auto Loader automatically keeps track of which files have already been read (incremental ingestion). This makes the pipeline incredibly cheap and fast, as it never needs to re-read old data.

* **Schema Inference & Evolution:** By setting `cloudFiles.inferColumnTypes` to `"true"` I avoid hardcoding a schema. The system dynamically adapts to the raw data, making the bronze layer robust to changes in the source system.

* **"Dumb" Bronze Layer:** The most important decision here is that the pipeline *doesnt* modify the data. The raw data is saved exactly as it is (SSOT - Single Source Of Truth). Bronze is only there to quickly get the data into Delta format and provide a historical backup if I need to rebuild Silver/Gold in the future.

### 3. Technical Details (The How)

* Uses the `cloudFiles` format to read files from the `/Volumes/marathos/default/raw/` volume.
* Supports both plain CSV files and pipeline-separated `.csv` files with headers.
* Uses the `@dlt.table` decorator to let Delta Live Tables orchestrate the execution.
