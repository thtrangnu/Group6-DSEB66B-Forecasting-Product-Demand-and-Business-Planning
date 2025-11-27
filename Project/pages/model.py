import dash
from dash import html, dcc

import numpy as np
import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error,
)

# =========================================================
# Register Page
# =========================================================
dash.register_page(__name__, path="/model", name="Model")

# =========================================================
# LOAD DATA
# =========================================================
df = pd.read_excel("data/data0979_enriched.xlsx")
df = df.sort_values(by="Date")

y = df["Total_Order_Demand"].values.reshape(-1, 1)
X = df.drop(columns=["Total_Order_Demand"])

# drop datetime
X = X.select_dtypes(exclude=["datetime64[ns]", "datetimetz"])

# one-hot
X = pd.get_dummies(X, drop_first=True)

X_np = X.values.astype(float)
y_np = y.astype(float)

total_rows = len(X_np)
num_blocks = 6
block_size = total_rows // num_blocks
test_size = 100
train_size = block_size - test_size

# =========================================================
# MANUAL NORMAL EQUATION
# =========================================================

X_with_bias = np.hstack((np.ones((X_np.shape[0], 1)), X_np))

X_test_blocks_manual = []
y_test_blocks_manual = []
y_pred_blocks_manual = []
R2_blocks_manual = []
SSE_blocks_manual = []
MSE_blocks_manual = []

block_id = 1

for start in range(0, total_rows, block_size):
    if start + block_size > total_rows:
        break

    X_train = X_with_bias[start:start+train_size]
    X_test  = X_with_bias[start+train_size:start+block_size]
    y_train = y_np[start:start+train_size]
    y_test  = y_np[start+train_size:start+block_size]

    XtX = X_train.T @ X_train
    Xty = X_train.T @ y_train
    beta = np.linalg.pinv(XtX) @ Xty

    y_pred = X_test @ beta

    residual = y_test - y_pred
    SSE = float(residual.T @ residual)
    MSE = SSE / len(y_test)
    SS_tot = float(np.sum((y_test - np.mean(y_test)) ** 2))
    R2 = 1 - SSE / SS_tot

    X_test_blocks_manual.append(X_test)
    y_test_blocks_manual.append(y_test)
    y_pred_blocks_manual.append(y_pred)
    R2_blocks_manual.append(R2)
    SSE_blocks_manual.append(SSE)
    MSE_blocks_manual.append(MSE)

    block_id += 1

metrics_manual_df = pd.DataFrame({
    "Block": list(range(1, 7)),
    "SSE": np.round(SSE_blocks_manual, 2),
    "MSE": np.round(MSE_blocks_manual, 2),
    "R²": np.round(R2_blocks_manual, 4)
})

# =========================================================
# SKLEARN MODELS
# =========================================================

def evaluate_model(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train.ravel())
    pred = model.predict(X_test)
    return (
        r2_score(y_test, pred),
        mean_absolute_error(y_test, pred),
        mean_squared_error(y_test, pred),
        np.sqrt(mean_squared_error(y_test, pred)),
        pred.reshape(-1,1)
    )

results = []
y_test_blocks = []
pred_LR = []
pred_DT = []
pred_RF = []

block_id = 1

for start in range(0, total_rows, block_size):
    if start + block_size > total_rows:
        break

    X_train = X_np[start:start+train_size]
    X_test  = X_np[start+train_size:start+block_size]
    y_train = y_np[start:start+train_size]
    y_test  = y_np[start+train_size:start+block_size]

    y_test_blocks.append(y_test)

    # LR
    r2_lr, mae_lr, mse_lr, rmse_lr, p_lr = evaluate_model(
        LinearRegression(), X_train, y_train, X_test, y_test
    )
    pred_LR.append(p_lr)
    results.append([block_id, "LinearRegression", r2_lr, mae_lr, mse_lr, rmse_lr])

    # DT
    r2_dt, mae_dt, mse_dt, rmse_dt, p_dt = evaluate_model(
        DecisionTreeRegressor(), X_train, y_train, X_test, y_test
    )
    pred_DT.append(p_dt)
    results.append([block_id, "DecisionTree", r2_dt, mae_dt, mse_dt, rmse_dt])

    # RF
    r2_rf, mae_rf, mse_rf, rmse_rf, p_rf = evaluate_model(
        RandomForestRegressor(n_estimators=100, random_state=42),
        X_train, y_train, X_test, y_test
    )
    pred_RF.append(p_rf)
    results.append([block_id, "RandomForest", r2_rf, mae_rf, mse_rf, rmse_rf])

    block_id += 1

results_df = pd.DataFrame(
    results,
    columns=["Block","Model","R2","MAE","MSE","RMSE"]
)

R2_LR = results_df[results_df.Model=="LinearRegression"]["R2"].values
R2_DT = results_df[results_df.Model=="DecisionTree"]["R2"].values
R2_RF = results_df[results_df.Model=="RandomForest"]["R2"].values

best_models_df = results_df.loc[
    results_df.groupby("Block")["R2"].idxmax(),
    ["Block","Model","R2"]
]

best_models_df.columns = ["Block","Best Model","R²"]

# =========================================================
# HELPER — ADD TABLE
# =========================================================
def make_table_from_df(df):
    header = [html.Th(col) for col in df.columns]
    rows = [
        html.Tr([html.Td(df.iloc[i,j]) for j in range(df.shape[1])])
        for i in range(df.shape[0])
    ]
    return html.Table(
        [html.Tr(header)] + rows,
        style={"width":"100%", "borderCollapse":"collapse"}
    )
# =========================================================
# PLOTS (Manual + sklearn)
# =========================================================

def plot_manual_blocks():
    fig = make_subplots(rows=2, cols=3,
                        subplot_titles=[f"Block {i}" for i in range(1,7)])
    for i in range(6):
        row = i//3 + 1
        col = i%3 + 1

        y_true = y_test_blocks_manual[i].flatten()
        y_pred = y_pred_blocks_manual[i].flatten()

        fig.add_trace(go.Scatter(
            x=list(range(len(y_true))),
            y=y_true,
            mode="lines",
            name="Actual",
            showlegend=(i==0)
        ), row=row, col=col)

        fig.add_trace(go.Scatter(
            x=list(range(len(y_pred))),
            y=y_pred,
            mode="lines",
            name="Predicted",
            line=dict(dash="dash"),
            showlegend=(i==0)
        ), row=row, col=col)

        fig.add_annotation(
            x=0.02, y=0.90,
            xref=f"x{i+1}", yref=f"y{i+1}",
            text=f"R² = {R2_blocks_manual[i]:.4f}",
            showarrow=False,
            bgcolor="white", opacity=0.7,
            font=dict(size=11)
        )

    fig.update_layout(
        height=650, template="plotly_white",
        title="Manual Linear Regression (Normal Equation) — 6 Rolling Blocks"
    )
    return fig


fig_manual_blocks = plot_manual_blocks()


# MODEL FIGURES
def plot_model_blocks(model_name, y_test_blocks, pred_blocks, R2_values):
    fig = make_subplots(rows=2, cols=3,
                        subplot_titles=[f"Block {i}" for i in range(1,7)])

    for i in range(6):
        row = i//3 + 1
        col = i%3 + 1

        yt = y_test_blocks[i].flatten()
        yp = pred_blocks[i].flatten()

        fig.add_trace(go.Scatter(
            x=list(range(len(yt))), y=yt,
            mode="lines", name="Actual",
            showlegend=(i==0)
        ), row=row, col=col)

        fig.add_trace(go.Scatter(
            x=list(range(len(yp))), y=yp,
            mode="lines", name="Predicted",
            line=dict(dash="dash"),
            showlegend=(i==0)
        ), row=row, col=col)

        fig.add_annotation(
            x=0.02, y=0.90,
            xref=f"x{i+1}", yref=f"y{i+1}",
            text=f"R² = {R2_values[i]:.4f}",
            showarrow=False,
            bgcolor="white", opacity=0.7,
            font=dict(size=11)
        )

    fig.update_layout(
        height=650,
        template="plotly_white",
        title=f"{model_name} — Actual vs Predicted (6 Blocks)"
    )
    return fig


fig_LR_blocks = plot_model_blocks("Linear Regression",
                                  y_test_blocks, pred_LR, R2_LR)
fig_DT_blocks = plot_model_blocks("Decision Tree",
                                  y_test_blocks, pred_DT, R2_DT)
fig_RF_blocks = plot_model_blocks("Random Forest",
                                  y_test_blocks, pred_RF, R2_RF)


# R2 Comparison Chart
fig_r2_compare = go.Figure()
blocks_range = list(range(1,7))

fig_r2_compare.add_trace(go.Scatter(
    x=blocks_range, y=R2_LR,
    mode="lines+markers",
    name="Linear Regression"
))
fig_r2_compare.add_trace(go.Scatter(
    x=blocks_range, y=R2_DT,
    mode="lines+markers",
    name="Decision Tree"
))
fig_r2_compare.add_trace(go.Scatter(
    x=blocks_range, y=R2_RF,
    mode="lines+markers",
    name="Random Forest"
))

fig_r2_compare.update_layout(
    title="R² Across Time Blocks (Model Comparison)",
    xaxis_title="Block",
    yaxis_title="R²",
    template="plotly_white"
)


# =========================================================
# FINAL LAYOUT
# =========================================================

layout = html.Div(
    className="page fade-in",
    children=[

        html.H2("Model Performance",
                className="section-title"),

        # I. Manual Normal Equation
        html.Div(
            className="data-card",
            children=[
                html.H3("I. Manual Linear Regression (using Normal Equation)",
                        className="sub-title"),
                dcc.Markdown(
                    """
The dataset is divided into **6 consecutive rolling blocks**.
Each block contains:

- **Train:** first 204 observations  
- **Test:** next 100 observations  
- Coefficients estimated using the **Normal Equation**  

For each block we compute **SSE, MSE, and R²**.
                    """
                ),
                make_table_from_df(metrics_manual_df),
                html.Br(),
                dcc.Graph(figure=fig_manual_blocks),
            ],
        ),

        # II. sklearn Models
        html.Div(
            className="data-card",
            children=[
                html.H3("II. Performance Comparison of 3 sklearn Models",
                        className="sub-title"),
                dcc.Markdown(
                    """
Models evaluated:

1. **LinearRegression**  
2. **DecisionTreeRegressor**  
3. **RandomForestRegressor**

Metrics:

- R²  
- MAE  
- MSE  
- RMSE  
                    """
                ),
                make_table_from_df(
                    results_df.round({"R2":4,"MAE":2,"MSE":2,"RMSE":2})
                ),
                html.Br(),
                html.H4("R² Across Blocks", className="sub-title"),
                dcc.Graph(figure=fig_r2_compare),
            ],
        ),

        # III. Actual vs Predicted
        html.Div(
            className="data-card",
            children=[
                html.H3("III. Actual vs Predicted (6 Blocks per Model)",
                        className="sub-title"),

                html.H4("1. Linear Regression"),
                dcc.Graph(figure=fig_LR_blocks),

                html.H4("2. Decision Tree", style={"marginTop":"25px"}),
                dcc.Graph(figure=fig_DT_blocks),

                html.H4("3. Random Forest", style={"marginTop":"25px"}),
                dcc.Graph(figure=fig_RF_blocks),
            ],
        ),

        # IV. Best Model Summary
        html.Div(
            className="data-card",
            children=[
                html.H3("IV. Best Performing Model per Block",
                        className="sub-title"),

                make_table_from_df(best_models_df.round({"R²":4})),
                html.Br(),

                dcc.Markdown(
                    f"""
### Summary
- **LinearRegression wins {int((best_models_df['Best Model']=='LinearRegression').sum())}/6 blocks**
- **DecisionTree wins {int((best_models_df['Best Model']=='DecisionTree').sum())}/6 blocks**
- **RandomForest wins 0/6 blocks**

### Insights
- LinearRegression is stable and performs best overall.
- DecisionTree captures some non-linear patterns but overfits.
- RandomForest is stable but does not outperform LinearRegression.

### Conclusion
**LinearRegression** is the most effective and interpretable baseline model  
for rolling time-series demand forecasting.
                    """
                ),
            ],
        ),
    ],
)

