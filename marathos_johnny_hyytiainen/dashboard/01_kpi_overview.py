# Script för att få en översikt av mina KPI siffror (totals, no shows, etc)
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
