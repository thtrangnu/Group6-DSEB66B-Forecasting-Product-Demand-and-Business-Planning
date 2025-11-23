import dash
from dash import html

dash.register_page(__name__, path="/about", name="Team")

layout = html.Div(
    className="page fade-in",
    children=[

        # ---------------- TEAM SECTION ----------------
        html.H2("Team Members", className="section-title"),

        html.Div(
            className="team-grid",
            children=[

                # ===== MEMBER 1 =====
                html.Div(
                    className="team-card",
                    children=[
                        html.Img(src="/assets/member1.png", className="member-img"),
                        html.H4("Lê Thị Thuỳ Trang"),
                        html.P("Leader"),
                        html.A(
                            "GitHub: thtrangnu",
                            href="https://github.com/thtrangnu",
                            target="_blank",
                            style={"color": "#2a72d4", "fontWeight": "600"}
                        ),
                    ],
                ),

                # ===== MEMBER 2 =====
                html.Div(
                    className="team-card",
                    children=[
                        html.Img(src="/assets/member2.png", className="member-img"),
                        html.H4("Vũ Thị Thu Trang"),
                        html.A(
                            "GitHub: vuthithutrang-jsu",
                            href="https://github.com/vuthithutrang-jsu",
                            target="_blank",
                            style={"color": "#2a72d4", "fontWeight": "600"}
                        ),
                    ],
                ),

                # ===== MEMBER 3 =====
                html.Div(
                    className="team-card",
                    children=[
                        html.Img(src="/assets/member3.png", className="member-img"),
                        html.H4("Vũ Thị Thuý Hằng"),
                        html.A(
                            "GitHub: thuyhang1607",
                            href="https://github.com/thuyhang1607",
                            target="_blank",
                            style={"color": "#2a72d4", "fontWeight": "600"}
                        ),
                    ],
                ),

                # ===== MEMBER 4 =====
                html.Div(
                    className="team-card",
                    children=[
                        html.Img(src="/assets/member4.png", className="member-img"),
                        html.H4("Ninh Duy Đức"),
                        html.A(
                            "GitHub: Duc-dev222",
                            href="https://github.com/Duc-dev222",
                            target="_blank",
                            style={"color": "#2a72d4", "fontWeight": "600"}
                        ),
                    ],
                ),

                # ===== MEMBER 5 =====
                html.Div(
                    className="team-card",
                    children=[
                        html.Img(src="/assets/member5.png", className="member-img"),
                        html.H4("Trần Viết Long"),
                        html.A(
                            "GitHub: 11245901",
                            href="https://github.com/11245901",
                            target="_blank",
                            style={"color": "#2a72d4", "fontWeight": "600"}
                        ),
                    ],
                ),

                # ===== MEMBER 6 =====
                html.Div(
                    className="team-card",
                    children=[
                        html.Img(src="/assets/member6.png", className="member-img"),
                        html.H4("Nguyễn Gia Khánh"),
                        html.A(
                            "GitHub: Khanh22082006",
                            href="https://github.com/Khanh22082006",
                            target="_blank",
                            style={"color": "#2a72d4", "fontWeight": "600"}
                        ),
                    ],
                ),
            ],
        ),

        # ---------------- PROJECT GITHUB SECTION ----------------
        html.H2("Project Repository", className="section-title"),

        html.Div(
            className="data-card",
            children=[
                html.P(
                    [
                        "GitHub Link: ",
                        html.A(
                            "Group6-DSEB66B-Forecasting-Product-Demand-and-Business-Planning",
                            href="https://github.com/thtrangnu/Group6-DSEB66B-Forecasting-Product-Demand-and-Business-Planning",
                            target="_blank",
                            style={"color": "#2a72d4", "fontWeight": "600"}
                        )
                    ]
                ),
            ],
        ),
    ],
)
