import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# Script för att få en översikt av growth over time sedan 1990 och framåt
# Läsa in data ifrån mina två growth marts i transformations/gold

df_growth = spark.sql("""
    SELECT 
        o.year_of_event,
        o.total_events_hosted,
        o.total_global_finishers  AS official_signups,
        v.total_global_finishers  AS verified_finishers
    FROM marathos.gold.mart_event_growth_official o
    JOIN marathos.gold.mart_event_growth_verified v
        ON o.year_of_event = v.year_of_event
    ORDER BY o.year_of_event ASC
""").toPandas()

# Using .copy() to avoid pandas SettingWithCopyWarning issues later on.
df_modern = df_growth[df_growth["year_of_event"] >= 1990].copy()


# Building my growth over time graphs focusing on option 2.
fig = make_subplots(specs = [[{"secondary_y": True}]])

# Vänster sida av y axis = antal events
fig.add_trace(
    go.Scatter(
        x = df_modern["year_of_event"],
        y = df_modern["total_events_hosted"],
        name = "Events hosted",
        mode = "lines+markers",
        line = dict(color = "#00CC96", width = 2)
    ),
    secondary_y = False
)

# Höger sida av y axis = antal finishers
fig.add_trace(
    go.Scatter(
        x = df_modern["year_of_event"],
        y = df_modern["official_signups"],
        name = "Official Signups",
        mode = "lines+markers",
        line = dict(color = "#EF553B", width = 2)
    ),
    secondary_y = True
)

fig.add_trace(
    go.Scatter(
        x=df_modern["year_of_event"],
        y=df_modern["verified_finishers"],
        name="Verified finishers",
        mode="lines+markers",
        line=dict(color="#636EFA", width=2, dash="dot")
    ),
    secondary_y=True
)

 # Layout and axis titles for my growth graph
fig.update_layout(
    title_text="Marathos — Global Growth 1990–2022",
    template="plotly_dark",
    height=450,
    hovermode="x unified"   # shows all values when hovering over a point in my graph
)

fig.update_yaxes(title_text="Events hosted", secondary_y=False)
fig.update_yaxes(title_text="Finishers", secondary_y=True)
fig.update_xaxes(title_text="Year")

fig.show()