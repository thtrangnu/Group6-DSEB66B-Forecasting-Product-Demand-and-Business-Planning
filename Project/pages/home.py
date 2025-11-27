import dash
from dash import html, dcc
import pandas as pd

dash.register_page(__name__, path="/", name="Home")

# === Load enriched data for quick stats ===
try:
    df = pd.read_excel("data/data0979_enriched.xlsx")
    n_rows, n_cols = df.shape
    date_min = pd.to_datetime(df["Date"]).min().date()
    date_max = pd.to_datetime(df["Date"]).max().date()
    zero_days = int((df["Total_Order_Demand"] == 0).sum())
    promo_days = int((df["Promotion"] == 1).sum())
except Exception:
    n_rows, n_cols = 0, 0
    date_min, date_max = "-", "-"
    zero_days = 0
    promo_days = 0

layout = html.Div(
    className="page fade-in",
    children=[

        # ===== HERO =====
        html.Section(
            className="hero",
            children=[
                html.H1("Demands Forecasting Dashboard", className="hero-title"),

                html.P(
                    "This dashboard provides a comprehensive end-to-end overview of the demand "
                    "forecasting project for Product_0979. It consolidates the entire analytical "
                    "pipeline, starting with raw data ingestion and moving through cleaning, "
                    "validation, and feature enrichment to ensure a reliable foundation for "
                    "analysis. The workflow continues with in-depth data storytelling, where the "
                    "historical demand patterns are interpreted through narrative insights — "
                    "including trends, seasonality, anomalies, and key demand drivers. This is "
                    "followed by the development of a linear regression model to estimate and "
                    "predict future demand. The dashboard also presents evaluation metrics, "
                    "visualizations of prediction performance, and final conclusions, providing "
                    "a clear and transparent view of how historical data is transformed into "
                    "actionable insights for planning and inventory optimization.",
                    className="hero-sub",
                ),
            ],
        ),

        # ===== PROJECT SUMMARY =====
        html.Div(
            className="data-card",
            children=[
                html.H2("Project Summary", className="section-title"),
                dcc.Markdown(
                    """
**Objective**

Forecast daily demand for **Product_0979** using historical transaction data,
combined with feature engineering (season, holidays, Black Friday, promotion)
and multivariate linear regression.

**Main Steps**

1. **Dataset** – filter Product_0979, clean invalid records, build a complete daily timeline.  
2. **Data Storytelling – Exploring the Data Through Narrative** – uncover the 5-year journey of Product_0979 through stories: silent days with zero demand, sudden explosive spikes, seasonal highs and lows, holiday effects, promotional surges, and anomaly clusters that reveal how the market behaves.  
3. **Model** – train and evaluate multivariate linear regression (and tree-based baselines).  
4. **Conclusion** – interpret model performance and provide business recommendations.
                    """
                ),
            ],
        ),

        # ===== TOP-LEVEL KPI =====
        html.H2("Dataset at a Glance", className="section-title"),

        html.Div(
            className="kpi-container",
            children=[
                html.Div(
                    className="kpi-card",
                    children=[
                        html.Div("Rows × Columns", className="kpi-label"),
                        html.Div(f"{n_rows} × {n_cols}", className="kpi-value blue"),
                    ],
                ),
                html.Div(
                    className="kpi-card",
                    children=[
                        html.Div("Date Range", className="kpi-label"),
                        html.Div(f"{date_min} → {date_max}", className="kpi-value"),
                    ],
                ),
                html.Div(
                    className="kpi-card",
                    children=[
                        html.Div("Zero-demand days", className="kpi-label"),
                        html.Div(f"{zero_days}", className="kpi-value"),
                    ],
                ),
                html.Div(
                    className="kpi-card",
                    children=[
                        html.Div("Promotion days", className="kpi-label"),
                        html.Div(f"{promo_days}", className="kpi-value"),
                    ],
                ),
            ],
        ),

        # ===== NAVIGATION GUIDE =====
        html.Div(
            className="data-card",
            children=[
                html.H3("How to Navigate this Dashboard"),
                dcc.Markdown(
                    """
- **Dataset** – see raw → cleaned → enriched data, with trend and feature engineering steps.  
- **Data Storytelling – Exploring the Data Through Narrative** – discover how Product_0979 behaves over 5 years through narrative insights: quiet days, explosive spikes, seasonal dynamics, holiday impacts, promotional effects, and anomaly clusters.  
- **Model** – regression metrics, model comparison, and actual vs predicted curves.  
- **Conclusion** – final assessment and business insights.  
- **About / Team** – project members and roles.
                    """
                ),
            ],
        ),
    ],
)
