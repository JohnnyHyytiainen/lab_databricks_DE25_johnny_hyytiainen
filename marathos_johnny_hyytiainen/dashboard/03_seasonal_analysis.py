import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# Script för att få insights över totala events i länder baserat på månad.
# Läsa in data ifrån min mart_seasonal_events_country

# 1: läsa in min data
df_seasonal = spark.sql("""
    SELECT 
        event_country,
        month,
        total_events,
        total_finishers,
        ROUND(avg_performance, 2) AS avg_performance
    FROM marathos.gold.mart_seasonal_events_country
    ORDER BY month ASC
""").toPandas()

# 2: Joina ländernas fulla namn från dim_country 
df_countries = spark.sql("""
    SELECT iso_code, country_name
    FROM marathos.gold.dim_country
""").toPandas()

df_seasonal = df_seasonal.merge(
    df_countries,
    left_on="event_country",
    right_on="iso_code",
    how="left"
)


# 3: Datasettets Top 50 länder
top_countries = (
    df_seasonal.groupby("country_name")["total_events"]
    .sum()
    .sort_values(ascending=False)
    .head(50)
    .index.tolist()
)

df_top = df_seasonal[df_seasonal["country_name"].isin(top_countries)]

# 4: Bygga min Graf med dropdown
fig = go.Figure()

for country in top_countries:
    df_country = df_top[df_top["country_name"] == country]
    
    fig.add_trace(go.Bar(
        x=df_country["month"],
        y=df_country["total_events"],
        name=country,
        visible=(country == top_countries[0])
    ))

buttons = []
for i, country in enumerate(top_countries):
    visible = [j == i for j in range(len(top_countries))]
    buttons.append(dict(
        label=country,
        method="update",
        args=[{"visible": visible}]
    ))

fig.update_layout(
    title_text="Total Number of Events in Dataset - Top 50 Nations",
    template="plotly_dark",
    height=450,
    xaxis=dict(
        title="Month",
        tickmode="array",
        tickvals=list(range(1, 13)),
        ticktext=["Jan","Feb","Mar","Apr","May","Jun",
                  "Jul","Aug","Sep","Oct","Nov","Dec"]
    ),
    yaxis_title="Total Events",
    updatemenus=[dict(
        active=0,
        buttons=buttons,
        x=1.0,
        y=1.15,
        xanchor="right"
    )]
)

fig.show()