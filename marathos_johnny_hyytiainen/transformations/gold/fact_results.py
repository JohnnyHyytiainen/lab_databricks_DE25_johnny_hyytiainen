from pyspark import pipelines as dp
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