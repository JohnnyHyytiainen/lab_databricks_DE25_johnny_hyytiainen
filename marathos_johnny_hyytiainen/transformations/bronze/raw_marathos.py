import re
from pyspark import pipelines as dp

# Hjälpfunktioner TODO: lyfta ut till min utils/schema_helpers.py
def to_snake_case(name):
    clean_name = re.sub(r"[^a-zA-Z0-9]", "_", name.strip())
    clean_name = re.sub(r"_+", "_", clean_name).casefold()
    return clean_name.rstrip("_")

def rename_columns_to_snake_case(df):
    new_columns = [to_snake_case(col) for col in df.columns]
    return df.toDF(*new_columns)

BASE_DIR = "/Volumes/marathos/default/raw"

# Declare min streaming table
@dp.table(
    name="raw_marathon_data", 
    comment="Bronze layer: Raw marathon data, columns formatted to snake_case.",
    table_properties={
        "delta.columnMapping.mode": "name",
        "delta.minReaderVersion": "2",
        "delta.minWriterVersion": "7"
    }
)
def create_raw_marathon_data():
    # Använd Auto Loader (cloudFiles) för stabil, incremental file streaming.
    # cloudFiles.inferColumnTypes -> slipper jag hårdkoda eller läsa schemat i förväg.
    df_raw_stream = (
        spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("header", "true")
        .option("cloudFiles.inferColumnTypes", "true") 
        .load(BASE_DIR)
    )
    
    # Kör dataframe genom snake case helper
    return rename_columns_to_snake_case(df_raw_stream)
