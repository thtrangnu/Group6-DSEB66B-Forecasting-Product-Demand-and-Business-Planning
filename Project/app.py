import dash
from dash import html
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title="Demands Prediction Dashboard"
)

# ⭐ Inject background.html vào cuối <body> bằng index_string
background_html = open("assets/background.html", "r", encoding="utf-8").read()

app.index_string = f"""
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
    </head>
    <body>
        {{%app_entry%}}

        <!-- ⭐ Our custom HTML injected here -->
        {background_html}

        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
"""

# ------------------------------------------------------
# Navbar
# ------------------------------------------------------
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Dataset", href="/dataset")),
        dbc.NavItem(dbc.NavLink("EDA", href="/eda")),
        dbc.NavItem(dbc.NavLink("Model", href="/model")),
        dbc.NavItem(dbc.NavLink("Conclusion", href="/conclusion")),
        dbc.NavItem(dbc.NavLink("About / Team", href="/about")),
    ],
    brand="Demands Prediction Dashboard",
    brand_href="/",
    color="#ffffff",
    dark=False,
    class_name="navbar-pastel"
)


# ------------------------------------------------------
# Layout
# ------------------------------------------------------
app.layout = html.Div(
    [
        navbar,
        html.Div(dash.page_container, className="page-container"),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
