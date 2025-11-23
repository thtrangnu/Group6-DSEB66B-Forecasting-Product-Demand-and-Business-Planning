import dash
from dash import html, dcc
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import numpy as np

dash.register_page(__name__, path="/eda", name="EDA")

df = pd.read_excel("data/data0979_enriched.xlsx")
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.month
df["Year"] = df["Date"].dt.year

# 1. Trend over time
fig_trend = px.line(
    df,
    x="Date",
    y="Total_Order_Demand",
    title="Total Order Demand over Time",
    markers=False,
)
fig_trend.update_layout(template="plotly_white")

# 2. Monthly mean
monthly_mean = (
    df.groupby("Month")["Total_Order_Demand"].mean().reset_index()
)
fig_month = px.line(
    monthly_mean,
    x="Month",
    y="Total_Order_Demand",
    markers=True,
    title="Average Demand by Month (2012–2016)",
)
fig_month.update_layout(template="plotly_white")

# 3. Season vs Year heatmap
pivot_season_year = df.pivot_table(
    values="Total_Order_Demand",
    index="Season",
    columns="Year",
    aggfunc="mean",
)
fig_season_year = px.imshow(
    pivot_season_year,
    text_auto=True,
    color_continuous_scale="YlGnBu",
    title="Average Demand by Season and Year",
)

# 4. Holiday vs Black Friday bar
holiday_mean = df.loc[df["Holiday"] == 1, "Total_Order_Demand"].mean()
bf_mean = df.loc[df["Black_Friday"] == 1, "Total_Order_Demand"].mean()

fig_holiday = px.bar(
    x=["Holiday", "Black Friday"],
    y=[holiday_mean, bf_mean],
    title="Average Demand on Holidays vs Black Friday",
)
fig_holiday.update_layout(template="plotly_white")

# 5. Boxplot by Season
fig_box = px.box(
    df,
    x="Season",
    y="Total_Order_Demand",
    title="Demand Distribution by Season",
)
fig_box.update_layout(template="plotly_white")

# 6. Correlation heatmap
corr = df[["Total_Order_Demand", "Order_Count", "Holiday", "Black_Friday", "Promotion"]].corr()
fig_corr = ff.create_annotated_heatmap(
    z=corr.values,
    x=list(corr.columns),
    y=list(corr.index),
    colorscale="RdBu",
    showscale=True,
)
fig_corr.update_layout(title="Correlation Matrix", template="plotly_white")

layout = html.Div(
    className="page fade-in",
    children=[
        html.H2("Exploratory Data Analysis (EDA)", className="section-title"),

        html.Div(
            className="data-card",
            children=[
                html.H3("Overview"),
                dcc.Markdown(
                    """
This page explores the demand pattern of **Product_0979** over time,
including long-term trend, seasonality, distribution and correlations
between engineered features (season, holiday, promotion, Black Friday).
                    """
                ),
            ],
        ),

        # 1. Trend
        html.H3("1. Demand Trend over Time", className="sub-title"),
        dcc.Graph(figure=fig_trend, className="chart-box"),

        # 2. Seasonality
        html.H3("2. Seasonality (Monthly & Seasonal Patterns)", className="sub-title"),
        dcc.Graph(figure=fig_month, className="chart-box"),
        dcc.Graph(figure=fig_season_year, className="chart-box"),

        # 3. Special Events
        html.H3("3. Special Events: Holidays vs Black Friday", className="sub-title"),
        dcc.Graph(figure=fig_holiday, className="chart-box"),

        # 4. Distribution
        html.H3("4. Demand Distribution by Season", className="sub-title"),
        dcc.Graph(figure=fig_box, className="chart-box"),

        # 5. Correlation
        html.H3("5. Correlation between Features", className="sub-title"),
        dcc.Graph(figure=fig_corr, className="chart-box"),
    ],
)


