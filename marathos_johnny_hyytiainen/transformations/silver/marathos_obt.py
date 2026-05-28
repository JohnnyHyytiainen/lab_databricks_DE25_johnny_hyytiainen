from pyspark import pipelines as dp
from pyspark.sql.functions import (
    col,
    coalesce,
    upper,
    lit,
    when,
    trim,
    regexp_replace,
    regexp_extract,
    split,
    right,
    expr,
    concat_ws,
    sha2 # Importera sha2 för hashning!
)

# Deklarera tabellen precis som i Bronze
@dp.table(
    name="silver.marathos_obt",
    comment="Silver OBT: Cleaned marathon data, distances split, countries extracted, strict schema."
)
def create_marathos_obt():
    df = dp.readStream("bronze.raw_marathon_data")
    
    df_silver = (
        df
        # === 1: event_name, event_country ===
        .withColumn("event_name", trim(regexp_replace(col("event_name"), '"', ""))) # Städa quotes
        .withColumn("event_country", upper(regexp_extract(col("event_name"), r"\(([^()]+)\)$", 1))) # Plocka ut ISO koderna och standardisera till CAPS

        # Tvätta bort landskod ifrån event_name, jag skriver över original column för att hålla det snyggt.
        .withColumn("event_name", trim(regexp_replace(col("event_name"), r"\s*\([^()]+\)$", "")))

        # === 2: Distances ===
        # event_length (siffra) och event_unit (Enhet)
        .withColumn("event_length", regexp_extract(col("event_distance_length"), r"^([\d\.]+)", 1).cast("double"))
        .withColumn("event_unit", regexp_extract(col("event_distance_length"), r"(?i)(km|mi|h)", 1))
        
        # === 3: Event dates ===
        # try_to_date via expr till DateType
        .withColumn("event_dates", expr("try_to_date(right(event_dates, 10), 'dd.MM.yyyy')"))
        .filter(col("event_dates").isNotNull())

        # === 4: KLUBB ===
        # Tvätta bort *
        .withColumn("athlete_club", trim(regexp_replace(col("athlete_club"), r"^\*+", "")))
        
        # === 5: Prestation, ålder och filtrering === 
        .filter(col("athlete_performance").isNotNull())
        .filter(~col("athlete_performance").rlike("(?i)d"))
        .withColumn("age_at_event", col("year_of_event") - col("athlete_year_of_birth"))
        .filter((col("age_at_event") >= 15) & (col("age_at_event") <= 100))

        # 5: Strippa alla bokstäver/mellanslag i slutet + tidskonvertering till double(HH:MM:SS)
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
        
        # === 6: Hastigheter -  Sanity check och athlete_average_speed till double ===
        .withColumn("athlete_average_speed", expr("try_cast(athlete_average_speed as double)"))
        .withColumn(
            "athlete_average_speed",
            when(col("athlete_average_speed") > 25.0, lit(None)).otherwise(col("athlete_average_speed")),
        )
        
        # === 7: Hantering av Nulls i data och Fallbacks ===
        .fillna("Missing", subset=["athlete_country", "athlete_gender", "athlete_age_category", "athlete_club", "event_country", "event_unit"])
        .withColumn("athlete_club", coalesce(trim(col("athlete_club")), lit("Missing")))
        .withColumn("athlete_year_of_birth", expr("try_cast(athlete_year_of_birth as int)"))
        .withColumn("athlete_id", expr("try_cast(athlete_id as int)"))
        .withColumn("athlete_id", when(col("athlete_id") <= 0, lit(None)).otherwise(col("athlete_id")))
        .withColumn("event_country", when(col("event_country") == "", lit("Missing")).otherwise(col("event_country")))
        .withColumn("athlete_country", when(col("athlete_country") == "", lit("Missing")).otherwise(col("athlete_country")))
        .withColumn("athlete_country", upper(col("athlete_country")))


        
        
        # === 8: Deduplication för streaming ===
        # Baserat på uppdaterade event_name ovan
        .dropDuplicates(["year_of_event", "event_name", "athlete_id"])
        
        # === 9: SKAPA SURROGATE KEYS (HASH) per KCs förslag ===
        # Eftersom event_name nu är städat och utan parenteser, blir IDt bra format
        .withColumn("event_id", sha2(concat_ws("||", col("event_name"), col("event_dates")), 256))
        .withColumn("result_id", sha2(concat_ws("||", col("athlete_id"), col("event_name"), col("year_of_event")), 256))
    )
    
    # === 10: Schema enforcement ===
    return df_silver.select(
        col("result_id").cast("string"),       # PK
        col("event_id").cast("string"),        # FK till Event Dimension
        col("athlete_id").cast("int"),         # FK till Athlete Dimension
        
        col("year_of_event").cast("int"),
        col("event_dates"), 
        col("event_name").cast("string"),
        col("event_country").cast("string"),   # regex-kolumn
        col("event_length").cast("double"),    # regex-kolumn (Siffran)
        col("event_unit").cast("string"),      # (Enheten km/mi/h)
        col("event_number_of_finishers").cast("int"),
        
        col("athlete_club").cast("string"),
        col("athlete_country").cast("string"),
        col("athlete_year_of_birth").cast("int"),
        col("athlete_gender").cast("string"),
        col("athlete_age_category").cast("string"),
        
        col("athlete_average_speed").cast("double"),
        col("performance").cast("double")
    )