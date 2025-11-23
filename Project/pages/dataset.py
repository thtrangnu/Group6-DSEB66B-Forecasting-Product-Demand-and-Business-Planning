import dash
from dash import html, dcc
import pandas as pd
import numpy as np
import plotly.graph_objects as go

dash.register_page(__name__, path="/dataset", name="Dataset")

# ====================================================
# (1) Filter & Clean Data (combined)
# ====================================================
df_raw = pd.read_excel("data/datasetprj.xlsx")

# --- Filter product 0979 ---
df_filtered = df_raw[df_raw["Product_Code"] == "Product_0979"]

# --- Aggregate daily ---
daily_demand = df_filtered.groupby("Date").agg(
    Total_Order_Demand=("Order_Demand", "sum"),
    Order_Count=("Product_Code", "count")
).reset_index()

# --- Sort and clean ---
df_clean = (
    daily_demand
    .sort_values(by="Date")
    .drop_duplicates(subset=["Date"], keep="first")
)

# Keep only valid demand
df_clean = df_clean[df_clean["Total_Order_Demand"] >= 0]

# Days with demand = 0 → order count = 0
df_clean.loc[df_clean["Total_Order_Demand"] == 0, "Order_Count"] = 0

df_clean["Date"] = pd.to_datetime(df_clean["Date"])
df_clean.to_excel("data/data0979_cleaned.xlsx", index=False)

# ====================================================
# (2) Plot Demand Trend
# ====================================================
fig_line = go.Figure()
fig_line.add_trace(go.Scatter(
    x=df_clean["Date"],
    y=df_clean["Total_Order_Demand"],
    mode="lines+markers",
    line=dict(color="#2a72d4", width=2),
    marker=dict(size=5)
))
fig_line.update_layout(
    title="Total Order Demand Over Time",
    xaxis_title="Date",
    yaxis_title="Total Order Demand",
    template="plotly_white",
)

# ====================================================
# (3) Feature Engineering (Enriched Dataset)
# ====================================================
df_enriched = df_clean.copy()
full_range = pd.date_range(start="2012-01-01", end="2016-12-31")

# Reindex to complete timeline
df_enriched = (
    df_enriched.set_index("Date")
    .reindex(full_range)
    .rename_axis("Date")
    .reset_index()
)

df_enriched["Total_Order_Demand"] = df_enriched["Total_Order_Demand"].fillna(0)
df_enriched["Order_Count"] = df_enriched["Order_Count"].fillna(0)

# --- Season ---
def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    return "Autumn"

df_enriched["Season"] = df_enriched["Date"].dt.month.apply(get_season)

# --- Holidays ---
def is_holiday(d):
    return int(
        (d.month == 1 and d.day == 1) or
        (d.month == 12 and d.day == 25)
    )

df_enriched["Holiday"] = df_enriched["Date"].apply(is_holiday)

# --- Black Friday ---
def get_black_friday(year):
    november = pd.date_range(f"{year}-11-01", f"{year}-11-30")
    thursdays = november[november.weekday == 3]
    thanksgiving = thursdays[3]
    return thanksgiving + pd.Timedelta(days=1)

black_fridays = [get_black_friday(y) for y in range(2012, 2017)]
df_enriched["Black_Friday"] = df_enriched["Date"].isin(black_fridays).astype(int)

# --- Promotion ---
threshold = df_enriched["Total_Order_Demand"].mean() + 2 * df_enriched["Total_Order_Demand"].std()
df_enriched["Promotion"] = (df_enriched["Total_Order_Demand"] >= threshold).astype(int)

df_enriched.to_excel("data/data0979_enriched.xlsx", index=False)

# ====================================================
# (4) Overview of Enriched Dataset
# ====================================================
overview_text = f"""
**Dataset Shape:** {df_enriched.shape[0]} rows × {df_enriched.shape[1]} columns  
**Date Range:** {df_enriched['Date'].min().date()} → {df_enriched['Date'].max().date()}  
**Zero-demand days:** {(df_enriched['Total_Order_Demand']==0).sum()}  
**Promotion spikes:** {(df_enriched['Promotion']==1).sum()}  
**Holiday count:** {(df_enriched['Holiday']==1).sum()}  
**Black Friday entries:** {(df_enriched['Black_Friday']==1).sum()}  
"""


preview_df = df_enriched.head(8)
preview_header = [html.Tr([html.Th(col) for col in preview_df.columns])]
preview_rows = [
    html.Tr([html.Td(preview_df.iloc[i][col]) for col in preview_df.columns])
    for i in range(len(preview_df))
]
preview_table = html.Table(preview_header + preview_rows, style={"width": "100%", "fontSize": "12px"})

# ====================================================
# Layout
# ====================================================

layout = html.Div(
    className="page fade-in",
    children=[

        html.H2("Dataset Overview", className="section-title"),

        # ====== Filter + Clean Combined ======
        html.Div(
            className="data-card",
            children=[
                html.H3("1. Data Filtering & Cleaning"),
                html.P("• Select product: Product_0979"),
                html.P("• Aggregate into daily total demand and order count"),
                html.P("• Remove duplicates and invalid values"),
                html.P("• Replace missing/zero-demand days properly"),
            ],
        ),

        html.H3("Demand Trend", className="sub-title"),
        dcc.Graph(figure=fig_line, className="chart-box"),

        html.Div(
            className="data-card",
            children=[
                html.H3("Trend Interpretation"),
                dcc.Markdown(
                    """
- Strong daily fluctuations suggest unstable demand patterns.  
- Multiple sudden peaks indicate effects of **promotions or special events**.  
- Several zero-demand days come from missing dates in the raw dataset → needed a complete timeline.  
- Feature engineering is required to uncover seasonal patterns and holiday effects.
                    """
                )
            ],
        ),

        # ===== Feature Engineering =====
        html.Div(
            className="data-card",
            children=[
                html.H3("2. Feature Engineering (Enriched Dataset)"),
                html.P("• Add full date range: 2012–2016"),
                html.P("• Add Season (Winter, Spring, Summer, Autumn)"),
                html.P("• Add international holidays (Jan 1, Dec 25)"),
                html.P("• Automatically detect Black Friday each year"),
                html.P("• Add Promotion flag based on statistical threshold"),
            ],
        ),

        # ===== Overview After Feature Engineering =====
        html.Div(
            className="data-card",
            children=[
                html.H3("3. Enriched Dataset Summary"),
                dcc.Markdown(overview_text)
            ]
        ),
        html.Div(
            className="data-card",
            children=[
                html.H3("4. Sample of Enriched Dataset"),
                preview_table,
            ],
        ),

    ]
)
