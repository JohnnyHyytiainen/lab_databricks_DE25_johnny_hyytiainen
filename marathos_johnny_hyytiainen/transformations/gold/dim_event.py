from pyspark import pipelines as dp

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

