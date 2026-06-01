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

df_gender = (
    df_demo[
        (df_demo["athlete_gender"].isin(["M", "F"])) &
        (df_demo["year_of_event"] >= 1990)
    ]
    .groupby(["year_of_event", "athlete_gender"])["total_unique_runners"]
    .sum()
    .reset_index()
)
    

fig = px.line(
    df_gender,
    x="year_of_event",
    y="total_unique_runners",
    color="athlete_gender",
    title="Gender Distribution of Runners 1990 – 2022",
    labels={
        "year_of_event": "Year",
        "total_unique_runners": "Unique Runners",
        "athlete_gender": "Gender"
    },
    template="plotly_dark",
    markers=True,
    color_discrete_map={"M": "#636EFA", "F": "#EF553B"}
)

fig.update_layout(
    height=450,
    hovermode="x unified"
)

fig.show()