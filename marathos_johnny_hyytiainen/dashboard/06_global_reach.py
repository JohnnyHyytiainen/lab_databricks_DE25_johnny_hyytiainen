import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# Script för att få insights över hur atleterna presterar och vilken global reach atleter har
# Läsa in data ifrån min mart_global_reach


df_reach = spark.sql("""
    SELECT
        iso_3166 AS iso_code,
        country_name,
        total_participants,
        national_avg_speed_kmh
    FROM marathos.gold.mart_global_reach
    ORDER BY total_participants DESC
""").toPandas()


fig = px.choropleth(
    df_reach,
    locations="iso_code",
    locationmode="ISO-3",  # Berättar för plotly att det är mina 3 letter codes som ska användas ifrån min dim_country
    color="total_participants",
    hover_name="country_name",
    # hover_data döljer min iso_code i tooltip eftersom att de redan finns i country_name via hover_name
    hover_data={
        "iso_code": False,
        "total_participants": ":,",
        "national_avg_speed_kmh": True,
    },
    color_continuous_scale="Viridis",
    title="Global Reach - Total Participants by Country",
    template="plotly_dark",
)

fig.update_layout(
    height=500,
    coloraxis_colorbar=dict(title="Participants", tickformat=","),
    geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"),
)

fig.show()
