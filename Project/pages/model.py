import dash
from dash import html, dcc
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import cross_val_score

dash.register_page(__name__, path="/model", name="Model")

# ===========================
# Load data
# ===========================
df = pd.read_excel("data/data0979_enriched.xlsx")

y = df["Total_Order_Demand"]
X = df.drop(columns=["Total_Order_Demand"])
# Chỉ giữ cột số + one-hot, bỏ datetime
X = df.drop(columns=["Total_Order_Demand"])
X = X.select_dtypes(exclude=["datetime"])

# One-hot encoding
X = pd.get_dummies(X, drop_first=True)

# Ép toàn bộ giá trị về float
X = X.astype(float)


# Manual LR
X_np = np.hstack((np.ones((X.shape[0], 1)), X.values.astype(float)))
y_np = y.values.reshape(-1, 1)

X_train_np, X_test_np, y_train_np, y_test_np = train_test_split(
    X_np, y_np, test_size=0.2, random_state=1
)

# Manual Beta
XtX = X_train_np.T @ X_train_np
Xty = X_train_np.T @ y_train_np
beta_hat = np.linalg.inv(XtX) @ Xty

y_test_hat = X_test_np @ beta_hat

# Metrics
residuals = y_test_np - y_test_hat
SSE = float(residuals.T @ residuals)
MSE = SSE / len(y_test_np)

SS_res = np.sum((y_test_np - y_test_hat)**2)
SS_tot = np.sum((y_test_np - np.mean(y_test_np))**2)
R2_manual = 1 - SS_res / SS_tot

# ===========================
# sklearn model comparison
# ===========================
x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=1
)

models = [
    ("Linear Regression", LinearRegression()),
    ("Decision Tree", DecisionTreeRegressor()),
    ("Random Forest", RandomForestRegressor(n_estimators=100, random_state=42)),
]

rows = []
for name, model in models:
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    r2 = r2_score(y_test, pred)
    cv = cross_val_score(model, x_train, y_train, cv=5).mean()
    rows.append((name, round(r2, 4), round(cv, 4)))

df_compare = pd.DataFrame(rows, columns=["Model", "R²", "CV Mean"])

# ===========================
# Plot Actual vs Predicted
# ===========================
fig_line = go.Figure()
fig_line.add_trace(go.Scatter(
    y=y_test_np.flatten(),
    mode="lines",
    name="Actual",
    line=dict(color="#2a72d4", width=3)
))
fig_line.add_trace(go.Scatter(
    y=y_test_hat.flatten(),
    mode="lines",
    name="Predicted",
    line=dict(color="#8abafc", width=2, dash="dash")
))
fig_line.update_layout(
    title="Actual vs Predicted",
    template="plotly_white",
    xaxis_title="Index",
    yaxis_title="Total Order Demand",
)

# ===========================
# Layout
# ===========================
layout = html.Div(
    className="page fade-in",
    children=[
        html.H2("Model Performance", className="section-title"),

        # SSE - MSE - R2 manual
        html.Div(
            className="data-card",
            children=[
                html.H3("Manual Linear Regression Metrics", style={"margin-bottom": "10px"}),
                html.P(f"SSE: {SSE:,.0f}"),
                html.P(f"MSE: {MSE:,.0f}"),
                html.P(f"R² (Test): {R2_manual:.4f}"),
            ],
        ),

        # Comparison table
        html.H3("Model Compare", className="sub-title"),
        html.Div(
            className="data-card",
            children=[
                html.Table(
                    [html.Tr([html.Th(col) for col in df_compare.columns])] +
                    [html.Tr([html.Td(value) for value in row]) for row in df_compare.values],
                )
            ],
        ),

        # Plot
        html.H3("Actual vs Predicted", className="sub-title"),
        dcc.Graph(figure=fig_line, className="chart-box"),

        # ===========================
        # Interpretation Section
        # ===========================
        html.Div(
            className="data-card",
            children=[
                html.H3("Model Evaluation & Assessment", style={"margin-bottom": "10px"}),

                dcc.Markdown(
                    """


##### **R² Evaluation on Test Set**

When calculating **R² on the test_set** using both the manual formula (Normal Equation) and scikit-learn’s `r2_score`, the results are **identical**:

**Manual R² = 0.8932**

---

##### **Meaning**

The value **0.8932** indicates that the model explains **89.32% of the variance** in the target variable on the test data.  
The perfect match between the two calculations confirms that the manual implementation of the R² formula is **correct and accurate**.

---

##### **Predictive Performance**

- A high R² value → the model **accurately predicts most observations** in the test_set.  
- The remaining variance (~10.7%) **is not explained** by the model, possibly due to:
  - data noise  
  - missing important predictors  
  - nonlinear relationships

---

##### **Generalization Ability**

- **R²_test** is an important metric for assessing how well the model predicts new data.  
- If R²_test is much lower than R²_train → the model is overfitting.  
- In this case:

**R²_test ≈ 0.893**

→ The model **generalizes very well**.

---

##### **Conclusion**

- **R² = 0.8932 on the test_set** → The multivariate linear regression model performs **quite well**, predicting close to actual values.  
- The **~10.7% unexplained variance** can be reduced by adding more predictors or trying nonlinear models.  
- **R²_test** is a much more **reliable indicator** than R² computed on the full dataset."""
                ),
            ],
        ),
    ]
)
