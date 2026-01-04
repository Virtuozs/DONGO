from dash import html, dcc
import dash_bootstrap_components as dbc

def layout():
    return html.Div(
        className="page",
        children=[

            # Header
            html.Div(
                className="header",
                children=[
                    html.Div("Global Energy Market Dashboard", className="title"),
                    html.Div("Spot Prices • Production • Infrastructure", className="subtitle")
                ]
            ),
            
            html.Div(
                className="card hero",
                children=[

                    # --- Card header ---
                    html.Div(
                        className="card-header",
                        children=[
                            html.Div("Spot Price", className="card-title"),

                            # Commodity selector INSIDE the card
                            dcc.RadioItems(
                                id="commodity-selector",
                                options=[
                                    {"label": "Oil", "value": "oil"},
                                    {"label": "Gas", "value": "gas"},
                                ],
                                value="oil",
                                inline=True,
                                className="commodity-toggle"
                            )
                        ]
                    ),

                    # --- Indicator text ---
                    html.Div(
                        id="price-indicator",
                        className="price-indicator"
                    ),

                    # --- Hero chart ---
                    dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False}
                    )
                ]
            ),


            # KPI row
            html.Div(
                className="kpi-row",
                children=[

                    html.Div(
                        className="kpi",
                        children=[
                            html.Div(
                                [
                                    html.Span("Global Oil Production"),
                                    dbc.Tooltip(
                                        "Total global crude oil and liquids production "
                                        "(latest year). Unit: thousand barrels per day. "
                                        "Source: Energy Institute Statistical Review.",
                                        target="oil-kpi-label"
                                    ),
                                    html.Span(" ℹ️", id="oil-kpi-label", className="info-icon")
                                ],
                                className="kpi-title"
                            ),
                            html.Div(id="oil-kpi", className="kpi-value"),
                            html.Div("Thousand barrels per day (kbd)", className="kpi-unit"),
                        ]
                    ),

                    html.Div(
                        className="kpi",
                        children=[
                            html.Div(
                                [
                                    html.Span("Global Gas Production"),
                                    dbc.Tooltip(
                                        "Total global natural gas production "
                                        "(latest year). Unit: billion cubic meters per year. "
                                        "Source: Energy Institute Statistical Review.",
                                        target="gas-kpi-label"
                                    ),
                                    html.Span(" ℹ️", id="gas-kpi-label", className="info-icon")
                                ],
                                className="kpi-title"
                            ),
                            html.Div(id="gas-kpi", className="kpi-value"),
                            html.Div("Billion cubic meters (bcm / year)", className="kpi-unit"),
                        ]
                    ),

                    html.Div(
                        className="kpi",
                        children=[
                            html.Div(
                                [
                                    html.Span("Facilities"),
                                    dbc.Tooltip(
                                        "Number of upstream oil & gas facilities "
                                        "tracked globally, including refineries, "
                                        "processing plants, and terminals. "
                                        "Source: Global Energy Monitor (OGIM).",
                                        target="fac-kpi-label"
                                    ),
                                    html.Span(" ℹ️", id="fac-kpi-label", className="info-icon")
                                ],
                                className="kpi-title"
                            ),
                            html.Div(id="facilities-kpi", className="kpi-value"),
                            html.Div("Infrastructure count", className="kpi-unit"),
                        ]
                    ),
                ]
            )
        ]
    )
