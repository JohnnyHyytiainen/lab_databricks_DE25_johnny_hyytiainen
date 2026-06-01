import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# Script för att få insights över demographics och prestationer
# Läsa in data ifrån min mart_demographics

# =======================
# Läsa in mina dataframes
# =======================
df_demo = spark.sql("""
    SELECT 
        year_of_event, 
        athlete_gender, 
        athlete_age_category, 
        athlete_country, 
        total_unique_runners, 
        total_races_completed 
    FROM marathos.gold.mart_demographics 
    ORDER BY year_of_event ASC
    """).toPandas()


df_age = (
    df_demo
    .groupby("athlete_age_category")["total_unique_runners"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

df_age_top = df_age.head(15)

fig = px.bar(
    df_age_top,
    x="athlete_age_category",
    y="total_unique_runners",
    title="Runner Distribution by Age Category",
    labels={
        "athlete_age_category": "Age Category",
        "total_unique_runners": "Total Unique Runners"
    },
    template="plotly_dark",
    color="total_unique_runners",
    color_continuous_scale="Blues"
)

fig.update_layout(
    height=450,
    xaxis_tickangle=-45,
    coloraxis_showscale=False
)

fig.show()