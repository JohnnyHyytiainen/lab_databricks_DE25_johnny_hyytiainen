from pyspark import pipelines as dp
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
from pyspark.sql.window import Window

# Deklarera tabellen precis som i Bronze
@dp.table(
    name="marathos_obt",
    comment="Silver OBT: Cleaned marathon data, dates fixed, nulls handled."
)
def create_marathos_obt():
    df = dp.read("raw_marathon_data")
    
    window_event = Window.orderBy("event_name")
    
    df_silver = (
        df
        # 1) Event name - Städa alla eventnamn till samma format (ta bort quotes)
        .withColumn("event_name", trim(regexp_replace(col("event_name"), '"', "")))
        
        # 2) Event dates - try_to_date via expr
        .withColumn("event_dates", expr("try_to_date(right(event_dates, 10), 'dd.MM.yyyy')"))
        .filter(col("event_dates").isNotNull())
        
        # 3) Filtrering av skräp i datan
        .filter(col("athlete_performance").isNotNull())
        .filter(~col("athlete_performance").rlike("(?i)d"))
        
        # 4) Kontroll av ålder
        .withColumn("age_at_event", col("year_of_event") - col("athlete_year_of_birth"))
        .filter((col("age_at_event") >= 15) & (col("age_at_event") <= 100))

        # 5) Strippa alla bokstäver/mellanslag i slutet
        .withColumn("perf_cleaned", trim(regexp_replace(col("athlete_performance"), "(?i)[a-z ]+$", "")))
        .withColumn("perf_split", split(col("perf_cleaned"), ":"))
        .withColumn(
            "performance",
            when(
                col("perf_cleaned").contains(":"),
                col("perf_split").getItem(0).cast("double")
                + (col("perf_split").getItem(1).cast("double") / 60.0)
                + (col("perf_split").getItem(2).cast("double") / 3600.0),
            ).otherwise(
                expr("try_cast(perf_cleaned as double)")
            ),
        )
        
        # 6) Hastigheter: Sanity check
        .withColumn("athlete_average_speed", expr("try_cast(athlete_average_speed as double)"))
        .withColumn(
            "athlete_average_speed",
            when(col("athlete_average_speed") > 25.0, lit(None)).otherwise(col("athlete_average_speed")),
        )
        
        # 7) Skapa RELEVANTA ID
        .withColumn("event_id", dense_rank().over(window_event))
        .withColumn("result_id", monotonically_increasing_id())
        .withColumn("athlete_id", expr("try_cast(athlete_id as int)"))
        
        # 8) Datatyper och fallbacks
        .withColumn("athlete_club", coalesce(trim(col("athlete_club")), lit("Unknown")))
        .withColumn("athlete_year_of_birth", expr("try_cast(athlete_year_of_birth as int)"))
        
        # 9) Städa upp temp och utdaterade kolumner
        .drop("age_at_event", "athlete_performance", "perf_cleaned", "perf_split")
    )
    
    return df_silver
