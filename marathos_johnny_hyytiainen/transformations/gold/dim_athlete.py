from pyspark import pipelines as dp

# ====== DIMENSIONER ======
# DIM_ATHLETE
# =========================
@dp.table(name="gold.dim_athlete", comment="Gold Dimension: Unique athletes")
def create_dim_athlete():
    return (
        spark.table("marathos.silver.marathos_obt")
        .select(
            "athlete_id",
            "athlete_club",
            "athlete_country",
            "athlete_year_of_birth",
            "athlete_gender",
            "athlete_age_category",
        )
        .dropDuplicates(["athlete_id"])
    )