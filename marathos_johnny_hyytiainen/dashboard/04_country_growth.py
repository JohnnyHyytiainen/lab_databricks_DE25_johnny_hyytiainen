import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# Script för att få insights över hur länderna växer när det kommer till antal events i datasettet
# Läsa in data ifrån min mart_global_growth

df_countries = spark.table("marathos.gold.dim_country").toPandas()
df_country_growth = spark.sql("""
    SELECT
        event_country,
        year,
        total_events,
        total_finishers
    FROM marathos.gold.mart_numb_events_country
    ORDER BY year ASC
""").toPandas()

# Block 1
df_country_growth = df_country_growth.merge(
    df_countries, left_on="event_country", right_on="iso_code", how="left"
)

# Block 2
df_modern = df_country_growth[df_country_growth["year"] >= 1990].copy()

top_10 = (
    df_modern.groupby("country_name")["total_events"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .index.tolist()
)

df_top10 = df_modern[df_modern["country_name"].isin(top_10)]
fig = go.Figure()

for country in top_10:
    df_c = df_top10[df_top10["country_name"] == country]

    fig.add_trace(
        go.Scatter(
            x=df_c["year"],
            y=df_c["total_events"],
            name=country,
            mode="lines+markers",
            visible=True,
        )
    )

buttons = [
    dict(
        label="All countries", method="update", args=[{"visible": [True] * len(top_10)}]
    )
]

for i, country in enumerate(top_10):
    visible = [j == i for j in range(len(top_10))]
    buttons.append(dict(label=country, method="update", args=[{"visible": visible}]))

fig.update_layout(
    title_text="Event Growth by Country 1990–2022 - Top 10 Nations",
    template="plotly_dark",
    height=450,
    xaxis_title="Year",
    yaxis_title="Total Events",
    hovermode="x unified",
    updatemenus=[dict(active=0, buttons=buttons, x=1.0, y=1.15, xanchor="right")],
)

fig.show()
