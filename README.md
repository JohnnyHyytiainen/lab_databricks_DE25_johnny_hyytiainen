# Marathos Data Platform
> Databricks lab - Data Engineering DE25, STI Stockholm

A full medallion architecture data platform built on Databricks, 
processing 200+ years of ultramarathon race data (7.4M records) 
from Bronze ingestion to Gold analytical marts and an interactive dashboard.

## Tech Stack
- **Platform:** Databricks (Unity Catalog, DLT Pipelines, Genie)
- **Processing:** PySpark, SQL
- **Visualization:** Plotly, Databricks Dashboard
- **Storage:** Delta Lake (Bronze -> Silver -> Gold)
- **Version Control:** Git + GitHub

## Architecture
```
Raw CSV -> Bronze (Auto Loader) -> Silver (OBT) -> Gold (Dims + Facts + Marts) -> Dashboard -> Genie
```

## Pipeline
| Layer | Description | Records |
|-------|-------------|---------|
| Bronze | Raw ingestion via Auto Loader (cloudFiles) | 7.46M |
| Silver | Cleaned OBT, surrogate keys, validated data | 6.8M |
| Gold | Star schema + 10 analytical marts | 82K events |

## Gold Layer
**Dimensions:** `dim_athlete`, `dim_event`, `dim_country` (bonus), `dim_date` (bonus)  
**Fact:** `fact_results`  
**Marts:** demographics, global reach, seasonal events, event growth (official + verified), distance breakdowns

## Bonus Tasks Completed
- `dim_country` - LLM-generated ISO country dataset with IOC historical codes
- `dim_date` - Full date dimension 1798–2100 with weekday support  
- LLM-generated synthetic marathon (Stockholm Marathos Ultra) streamed through full pipeline
- Dashboard with comprehensive insights across 4 pages
- Marathos Genie with 10+ verified test queries
- `Fail Fast`-pivot: Evaluated custom Plotly embeddings for dashboard but pivoted to native Databricks Lakeview/Genie to optimize for platform constraints and delivery time. It did not work out as intended because of Free User constraints.

## Key Insights
- Covid-19 caused a 57% drop in events (2019 -> 2020), visible across all nations
- October and September are global prime time months for ultramarathons
- 81% of race starts are male athletes, but female participation grew 40x since 1980
- Weekends account for 91% of all events (Saturday dominant)
- Ethiopia leads in average speed (12.82 km/h) despite lower participation

## Data Notes
- `athlete_average_speed` capped at 25 km/h (sanity check based on world records)
- Country codes follow IOC standards - historical nations preserved (URS, YUG etc.)
- No-show rate: 8.6% (official signups vs verified finishers)


## Repository Structure
```
lab_databricks_DE25_johnny_hyytiainen
├─ docs/
│  └─ notes/                          # Architectural decisions & learnings (example: avoiding Fan Traps)
│     ├─ fan_trap.md                  # Docs regarding Fan trap and thoughts about it.
│     └─ sources.md                   # Sources for academic transparency.  
│
├─ marathos_johnny_hyytiainen/
│  ├─ dimensional_modeling/
│  │  └─ marathos_pdm.png             # Final Physical Data Model (Snowflake Schema)
│  │
│  │
│  ├─ dashboard/
│  │  └─ 01_*.py                      # Scripts to attempt creating custom Plotly embeddings for dashboard
│  │
│  ├─ explorations/
│  │  ├─ 01_eda_bronze.ipynb          # Raw data discovery and profiling
│  │  ├─ 02_eda_silver.ipynb          # Data cleaning logic & quality rules testing
│  │  └─ 04_dashboard_creating.ipynb  # Plotly/Pandas logic drafts for dashboard KPIs
│  │
│  ├─ setup/
│  │  └─ setup_unity_catalog.sql      # DDL for setting up Catalogs and Schemas
│  │
│  ├─ transformations/                # Core Data Pipeline (Medallion Architecture)
│  │  ├─ bronze/
│  │  │  └─ raw_marathos.py           # Ingestion layer (Raw -> Bronze)
│  │  │
│  │  ├─ silver/
│  │  │  └─ marathos_obt.py           # Cleaned & validated One-Big-Table layer
│  │  │
│  │  └─ gold/
│  │     ├─ dim_*.py                  # Dimension tables (Spark: Athlete, Event, Country, Date)
│  │     ├─ fact_results.py           # Granular fact table (Spark)
│  │     └─ mart_*.sql                # Aggregated views for BI/Genie (SQL: Growth, Demographics etc.)
│  │
│  └─ utils/
│     └─ schema_helpers.py            # Helper functions for PySpark schemas
├─ pyproject.toml
└─ README.md
``` 