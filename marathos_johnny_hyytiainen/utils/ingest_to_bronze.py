import re
from pyspark.sql import SparkSession

# --- 1: Helpers (Direkt i skriptet för att undvika import-strul) ---
def to_snake_case(name):
    clean_name = re.sub(r"[^a-zA-Z0-9]", "_", name.strip())
    clean_name = re.sub(r"_+", "_", clean_name).casefold()
    return clean_name.rstrip("_")

def rename_columns_to_snake_case(df):
    new_columns = [to_snake_case(col) for col in df.columns]
    return df.toDF(*new_columns)

spark = SparkSession.builder.getOrCreate()

# --- 2: Paths ---
FILE_PATH = "/Volumes/marathos/default/raw/TWO_CENTURIES_OF_UM_RACES.csv"
BRONZE_TABLE_NAME = "marathos.bronze.raw_marathon_data"

# --- 3: Läs in raw data ---
df_raw = spark.read.csv(FILE_PATH, header=True, inferSchema=True)

# --- 4: Formatera hela schemat ---
df_bronze = rename_columns_to_snake_case(df_raw)

# --- 5: Ingesta min data till Delta Lake ---
print(f"Writing formatted raw data to: {BRONZE_TABLE_NAME}")

(df_bronze.write
 .format("delta")
 .mode("overwrite")
 .saveAsTable(BRONZE_TABLE_NAME))

print("Bronze ingestion is Done. The Schema now uses snake_case and is ready for Silver")