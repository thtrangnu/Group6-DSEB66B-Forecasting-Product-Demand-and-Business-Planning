import dash
from dash import html, dcc

dash.register_page(__name__, path="/conclusion", name="Conclusion")

layout = html.Div(
    className="page fade-in",
    children=[

        html.H2("Conclusion", className="section-title"),

        # 1. Model Performance
        html.Div(
            className="data-card",
            children=[
                html.H3("1. Overall Model Performance"),
                dcc.Markdown(
                    """
The multivariate linear regression model achieves an **R² of about 0.89**
on the test set, meaning it explains roughly **89% of the variance** in daily demand.
Actual vs predicted curves are closely aligned, indicating strong predictive power
without obvious signs of overfitting.
                    """
                ),
            ],
        ),

        # 2. Key insights
        html.Div(
            className="data-card",
            children=[
                html.H3("2. Key Insights from EDA"),
                dcc.Markdown(
                    """
- Demand shows **strong fluctuations** with occasional spikes.  
- **Seasonality** exists: certain seasons/months have consistently higher demand.  
- **Special events** such as Black Friday generate clear demand peaks.  
- **Promotion days** correspond strongly to high-demand spikes.
                    """
                ),
            ],
        ),

        # 3. Business impacts
        html.Div(
            className="data-card",
            children=[
                html.H3("3. Business Implications"),
                dcc.Markdown(
                    """
- The model can support **inventory planning** for Product_0979.  
- Demand peaks around holidays and promotions should be met with **increased stock levels**.  
- Extended low-demand periods may indicate opportunities for **cost reduction efforts**.
                    """
                ),
            ],
        ),

        # 4. Limits + Future work
        html.Div(
            className="data-card",
            children=[
                html.H3("4. Limitations & Future Work"),
                dcc.Markdown(
                    """
- The model uses only **historical demand and calendar-based features**.  
  → It does not incorporate price, competitor behavior, weather, or economic factors.  
- The dataset contains many **zero-demand days**, making subtle patterns harder to detect.

**Future improvements:**

- Integrate external factors (price, holidays, marketing campaigns, weather).  
- Test more advanced models (e.g., **Random Forest, Gradient Boosting, LSTM**).  
- Deploy a real-time forecasting pipeline for daily or weekly planning.
                    """
                ),
            ],
        ),

        # 5. Interpretation of Model Behavior
        html.Div(
            className="data-card",
            children=[
                html.H3("5. Interpretation of Model Behavior"),
                dcc.Markdown(
                    """
Although the model performs well, several behavior patterns are important to understand:

- Demand spikes are difficult for linear regression to capture precisely.  
- Heavy dependence on calendar features means the model performs best when demand follows
  regular seasonal or promotional cycles.  
- A high number of **zero-demand days** reduces the model’s ability to learn finer trends.  
- Events like holidays or Black Friday have **large coefficients** because they produce rare but strong effects.
                    """
                ),
            ],
        ),

        # 6. Comparison with Simple Baselines
        html.Div(
            className="data-card",
            children=[
                html.H3("6. Comparison with Baseline Approaches"),
                dcc.Markdown(
                    """
- **Mean predictor**: cannot capture seasonality or promotions.  
- **Last value (naive)**: fails because many days have zero demand.  
- **Moving average**: too smooth and fails to react to sudden promotional peaks.

Compared to these baselines, linear regression delivers **substantially higher accuracy**.
                    """
                ),
            ],
        ),

        # 7. Reliability & Generalization
        html.Div(
            className="data-card",
            children=[
                html.H3("7. Reliability & Generalization"),
                dcc.Markdown(
                    """
- The test R² closely matches training performance, showing **no overfitting**.  
- Feature effects remain stable over time.  
- The model generalizes well for **short-term operational planning** 
  as long as future data follows similar patterns.
                    """
                ),
            ],
        ),

        # 8. Practical Business Recommendations
        html.Div(
            className="data-card",
            children=[
                html.H3("8. Practical Recommendations for Business"),
                dcc.Markdown(
                    """
##### **Inventory & Supply Chain**
- Increase stock ahead of holidays and promotions.  
- Adjust procurement using predicted weekly demand.

##### **Marketing Optimization**
- Plan promotions strategically to avoid stockouts.  
- Use low-demand periods for targeted marketing.

##### **Operational Efficiency**
- Reduce overstock during long zero-demand sequences.  
- Use demand trend as a guide for better warehouse planning.
                    """
                ),
            ],
        ),
    ],
)
