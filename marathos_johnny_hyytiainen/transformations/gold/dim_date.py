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
        .withColumn("day_of_week", dayofweek(col("date")))
        .withColumn(
            "is_weekend",
            when(dayofweek(col("date")).isin([1, 7]), lit(True)).otherwise(lit(False)),
        )
    )