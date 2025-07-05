import os
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go

BASE = Path(__file__).resolve().parent.parent
DATA_DIR = BASE / "data"
OUT_DIR = BASE / "outputs"
OUT_DIR.mkdir(exist_ok=True)

sales = pd.read_csv(DATA_DIR / "sales_data.csv", parse_dates=["month"])
local = pd.read_csv(DATA_DIR / "local_sales_data.csv", parse_dates=["date"])

palette = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a"]

fig1 = go.Figure()
for i, reg in enumerate(sales.region.unique()):
    region_data = sales[sales.region == reg]
    fig1.add_trace(
        go.Scatter(
            x=region_data.month,
            y=region_data.revenue_kUSD,
            mode="lines",
            stackgroup="one",
            name=reg,
            line=dict(width=0.5, color=palette[i]),
        )
    )

fig1.update_layout(
    title="<b>2024 Monthly Revenue by Region (kUSD)</b>",
    xaxis_title="Month",
    yaxis_title="Revenue (thousand USD)",
    legend_title="Region",
    legend=dict(bordercolor="black", borderwidth=1, orientation="h", y=-0.25),
    margin=dict(t=70, l=60, r=40, b=80),
)

top10 = (
    local.groupby("store_id", as_index=False)
    .agg(total_rev=("revenue_kUSD", "sum"))
    .nlargest(10, "total_rev")
    .sort_values("total_rev")
)

fig2 = go.Figure(
    go.Bar(
        x=top10.total_rev,
        y=top10.store_id,
        orientation="h",
        marker_color=palette[1],
    )
)

fig2.update_layout(
    title="<b>Top‑10 Stores – 2024 Revenue (kUSD)</b>",
    xaxis_title="Revenue (thousand USD)",
    yaxis_title="Store ID",
    legend_title_text="",
    margin=dict(t=70, l=100, r=40, b=60),
)

dash_html = f"""
<html>
    <head>
        <meta charset="utf-8"/>
        <title>Golden Image Dashboard</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: 'Open Sans', sans-serif; margin:40px; }}
            .chart {{ width: 100%; max-width: 900px; margin: auto; }}
        </style>
    </head>
    <body>
        <h1 style="text-align:center;"><b>Company Sales Dashboard – 2024</b></h1>
        <div class="chart" id="fig1"></div>
        <div class="chart" id="fig2"></div>
        <script>
            var fig1 = {fig1.to_json()};
            var fig2 = {fig2.to_json()};
            Plotly.newPlot('fig1', fig1.data, fig1.layout);
            Plotly.newPlot('fig2', fig2.data, fig2.layout);
        </script>
    </body>
</html>
"""

with open(OUT_DIR / "golden_image.html", "w", encoding="utf-8") as f:
    f.write(dash_html)

print("Dashboard created at", OUT_DIR / "golden_image.html")
