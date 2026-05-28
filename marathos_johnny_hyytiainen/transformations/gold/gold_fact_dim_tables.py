from pyspark import pipelines as dp
from pyspark.sql.functions import (
    col,
    explode,
    sequence,
    to_date,
    year,
    month,
    dayofmonth,
    dayofweek,
    when,
    lit,
)


# ====== DIMENSIONER ======
# DIM_ATHLETE
# =========================
@dp.table(name="gold.dim_athlete", comment="Gold Dimension: Unique athletes")
def create_dim_athlete():
    return (
        spark.table("marathos.silver.marathos_obt")
        .select(
            "athlete_id",
            "athlete_club",
            "athlete_country",
            "athlete_year_of_birth",
            "athlete_gender",
            "athlete_age_category",
        )
        .dropDuplicates(["athlete_id"])
    )


# ====== DIMENSIONER ======
# DIM_EVENT
# =========================
@dp.table(name="gold.dim_event", comment="Gold Dimension: Unique Events")
def create_dim_event():
    return (
        spark.table("marathos.silver.marathos_obt")
        .select(
            "event_id",
            "event_name",
            "event_dates",
            "event_country",
            "event_length",
            "event_unit",
            "event_number_of_finishers",
        )
        .dropDuplicates(["event_id"])
    )


# ====== DIMENSIONER ======
# DIM_COUNTRY (BONUS TASK)
# =========================
@dp.table(
    name="gold.dim_country", comment="Gold Dimension: ISO country mapping (BONUS TASK)"
)
def create_dim_country():
    return (
        spark.read.format("csv")
        .option("header", "true")
        .load("/Volumes/marathos/default/raw/dim_countries.csv")
    )


# ====== DIMENSIONER ======
# DIM_DATE (BONUS TASK)
# =========================
@dp.table(
    name="gold.dim_date",
    comment="Gold Dimension: Date dimension for BI filtering (BONUS TASK)",
)
def create_dim_date():
    # Genererar automatiskt alla datum från 1798-01-01 till 2100-12-31
    df_dates = spark.sql(
        "SELECT explode(sequence(to_date('1798-01-01'), to_date('2100-12-31'), interval 1 day)) AS date"
    )
    return (
        df_dates.withColumn("year", year(col("date")))
        .withColumn("month", month(col("date")))
        .withColumn("day", dayofmonth(col("date")))
        # dayofweek returnerar 1 för Söndag, 7 för Lördag
        .withColumn(
            "is_weekend",
            when(dayofweek(col("date")).isin([1, 7]), lit(True)).otherwise(lit(False)),
        )
    )


# ====== FACT TABLE ======
#       FACT_RESULTS
# ========================
@dp.table(
    name="gold.fact_results", comment="Gold Fact table: Athlete performances/results"
)
def create_fact_results():
    return spark.table("marathos.silver.marathos_obt").select(
        "result_id",
        "event_id",
        "athlete_id",
        "year_of_event",
        "performance",
        "athlete_average_speed",
    )
