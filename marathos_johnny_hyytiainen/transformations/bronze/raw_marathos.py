from utils.schema_helpers import rename_columns_to_snake_case
from pyspark.sql import SparkSession

# 1. Definiera sökvägar
FILE_PATH = "/Volumes/marathos/default/raw/TWO_CENTURIES_OF_UM_RACES.csv"
BRONZE_TABLE_NAME = "marathos.bronze.raw_marathon_data"

# 2. Läs in rådatan
df_raw = spark.read.csv(FILE_PATH, header=True, inferSchema=True)

# 3. Formatera schemat (inga ändringar i själva raderna, endast kolumnnamn)
df_bronze = rename_columns_to_snake_case(df_raw)

# 4. Ingest till Delta Lake
print(f"Writing formatted raw data to: {BRONZE_TABLE_NAME}")
(df_bronze.write.format("delta").mode("overwrite").saveAsTable(BRONZE_TABLE_NAME))

print(
    "Bronze ingestion is Done. The Schema now uses snake_case and is ready for Silver"
)
