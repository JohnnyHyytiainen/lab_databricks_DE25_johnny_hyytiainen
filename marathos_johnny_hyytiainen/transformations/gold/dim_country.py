from pyspark import pipelines as dp

# ====== DIMENSIONER ======
# DIM_COUNTRY (BONUS TASK)
# =========================
@dp.table(
    name="gold.dim_country", comment="Gold Dimension: ISO country mapping (BONUS TASK)"
)
def create_dim_country():
    return (
        spark.read.format("csv")
        .option("header", "true")
        .load("/Volumes/marathos/default/raw/dim_countries.csv")
    )