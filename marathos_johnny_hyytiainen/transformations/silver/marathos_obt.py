from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    coalesce,
    lit,
    when,
    trim,
    regexp_replace,
    dense_rank,
    monotonically_increasing_id,
    split,
    right,
    expr,
)
from pyspark.sql.types import IntegerType, DoubleType
from pyspark.sql.window import Window

spark = SparkSession.builder.getOrCreate()

SILVER_TABLE_NAME = "marathos.silver.marathos_obt"

# Läs in data ifrån från Bronze
df = spark.sql("SELECT * FROM marathos.bronze.raw_marathon_data")
window_event = Window.orderBy("event_name")
print("Beginning ETL process to clean data to Silver OBT.")

df_silver = (
    df
    # 1) Event name - Städa alla eventnamn till samma format (ta bort quotes)
    .withColumn("event_name", trim(regexp_replace(col("event_name"), '"', "")))
    
    # 2) Event dates - try_to_date via expr för att hantera ogiltiga datum, skeva datum gör jag till Null istället för krasch
    .withColumn("event_dates", expr("try_to_date(right(event_dates, 10), 'dd.MM.yyyy')"))
    .filter(col("event_dates").isNotNull())
    
    # 3) Filtrering av skräp i datan
    .filter(col("athlete_performance").isNotNull())
    .filter(~col("athlete_performance").rlike("(?i)d"))
    
    # 4) Kontroll av ålder (Rensar automatiskt nulls i year of birth)
    .withColumn("age_at_event", col("year_of_event") - col("athlete_year_of_birth"))
    .filter((col("age_at_event") >= 15) & (col("age_at_event") <= 100))

    # 5) Strippa alla bokstäver/mellanslag i slutet oavsett enhet (km/mi/h/d)
    .withColumn("perf_cleaned", trim(regexp_replace(col("athlete_performance"), "(?i)[a-z ]+$", "")))
    .withColumn("perf_split", split(col("perf_cleaned"), ":"))
    .withColumn(
        "performance",
        when(
            col("perf_cleaned").contains(":"), # Om det finns ett kolon är det ett tidsformat (HH:MM:SS)
            col("perf_split").getItem(0).cast(DoubleType())
            + (col("perf_split").getItem(1).cast(DoubleType()) / 60.0)
            + (col("perf_split").getItem(2).cast(DoubleType()) / 3600.0),
        ).otherwise(
            expr("try_cast(perf_cleaned as double)") # try_cast gör det säkert för krasch om det är en ren distans siffra någonstans
        ),
    )
    
    # 6) Hastigheter: Sanity check. Allt över 25 km/h är ogiltigt/skräp -> Null(Se 02_eda_silver)
    .withColumn("athlete_average_speed", expr("try_cast(athlete_average_speed as double)"))
    .withColumn(
        "athlete_average_speed",
        when(col("athlete_average_speed") > 25.0, lit(None)).otherwise(col("athlete_average_speed")),
    )
    
    # 7) Skapa RELEVANTA ID
    .withColumn("event_id", dense_rank().over(window_event))
    .withColumn("result_id", monotonically_increasing_id())
    .withColumn("athlete_id", expr("try_cast(athlete_id as int)"))
    
    # 8) Datatyper och fallbacks till Unknown
    .withColumn("athlete_club", coalesce(trim(col("athlete_club")), lit("Unknown")))
    .withColumn("athlete_year_of_birth", expr("try_cast(athlete_year_of_birth as int)"))
    
    # 9) Städa upp temp och utdaterade kolumner
    .drop("age_at_event", "athlete_performance", "perf_cleaned", "perf_split")
)

# Ingest datan till Silver
print(f"Writing clean OBT TO: {SILVER_TABLE_NAME}")

(
    df_silver.write.format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(SILVER_TABLE_NAME)
)

print("Silver OBT is written. Dates are fixed, speeds are saved, Nulls handled and IDs created")
