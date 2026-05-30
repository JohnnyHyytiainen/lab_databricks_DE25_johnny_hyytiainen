import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# Script för att få en översikt av mina KPI siffror (totals, no shows, etc)
# Läsa in data ifrån mina två growth marts i transformations/gold
df_official = spark.sql(
    """
    SELECT 
        SUM(total_events_hosted) AS total_events,
        SUM(total_global_finishers) AS total_finishers
    FROM marathos.gold.mart_event_growth_official"""
).toPandas()

df_verified = spark.sql(
    """
    SELECT 
        SUM(total_global_finishers) AS verified_finishers
    FROM marathos.gold.mart_event_growth_verified"""
).toPandas()

# Mina DataFrames för att bygga mina KPI kort
total_events = int(df_official["total_events"].iloc[0])
total_finishers = int(df_official["total_finishers"].iloc[0])

verified = int(df_verified["verified_finishers"].iloc[0])
no_show_rate = round((total_finishers - verified) / total_finishers * 100, 1)


# Byggandet av mina KPI kort
fig = make_subplots(rows=1, cols=4, specs=[[{"type": "indicator"}] * 4])

# Total events KPI
fig.add_trace(
    go.Indicator(
        mode="number",
        value=total_events,
        title={"text": "Total Events<br><span style='font-size:0.8em'>All time</span>"},
        number={"valueformat": ","},
    ),
    row=1,
    col=1,
)

# Total finishers KPI
fig.add_trace(go.Indicator(
    mode="number",
    value=total_finishers,
    title={"text": "Official Finishers<br><span style='font-size:0.8em'>Reported by organizers</span>"},
    number={"valueformat": ","}
), row=1, col=2)

# Verified finishers KPI
fig.add_trace(go.Indicator(
    mode="number",
    value=verified,
    title={"text": "Verified Results<br><span style='font-size:0.8em'>In our database</span>"},
    number={"valueformat": ","}
), row=1, col=3)

# No show rate KPI
fig.add_trace(go.Indicator(
    mode="number",
    value=no_show_rate,
    title={"text": "No-Show Rate<br><span style='font-size:0.8em'>Official vs Verified</span>"},
    number={"suffix": "%", "valueformat": ".2f"}
), row=1, col=4)

# Updatera layouten, storlek, margins och titel
fig.update_layout(
    title_text="Marathos Global Overview KPIs",
    template="plotly_dark", # Vilken färg template som används
    height=250,
    margin=dict(t=85, b=20, l=20, r=20)
)

fig.show()