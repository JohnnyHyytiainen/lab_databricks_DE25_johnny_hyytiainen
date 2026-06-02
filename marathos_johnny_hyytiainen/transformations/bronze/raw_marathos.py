import re
from pyspark import pipelines as dp
from utils.schema_helpers import rename_columns_to_snake_case

BASE_DIR = "/Volumes/marathos/default/raw"

# Declare min streaming table
@dp.table(
    name="bronze.raw_marathon_data", 
    comment="Bronze layer: Raw marathon data, columns formatted to snake_case.",
    table_properties={
        "delta.columnMapping.mode": "name",
        "delta.minReaderVersion": "2",
        "delta.minWriterVersion": "7"
    }
)
def create_raw_marathon_data():
    # Använder Auto Loader (cloudFiles) för stabil, incremental file streaming.
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
