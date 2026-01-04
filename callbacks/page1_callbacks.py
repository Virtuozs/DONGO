from dash import Input, Output
import plotly.graph_objects as go
from db import query

def register_callbacks(app):

    @app.callback(
        Output("price-chart", "figure"),
        Input("commodity-selector", "value")
    )
    
    def update_price_chart(commodity):

        if commodity == "oil":
            df = query("""
                SELECT date, price, benchmark
                FROM price
                WHERE benchmark IN ('Brent', 'WTI')
                ORDER BY date
            """)

            fig = go.Figure()

            colors = {
                "Brent": "#E45756",
                "WTI": "#4C78A8",
            }

            for name, color in colors.items():
                sub = df[df["benchmark"] == name]
                fig.add_trace(
                    go.Scatter(
                        x=sub["date"],
                        y=sub["price"],
                        name=name,
                        mode="lines",
                        line=dict(width=2.5, color=color),
                        hovertemplate=
                            f"<b>{name}</b><br>" +
                            "Date: %{x|%Y-%m-%d}<br>" +
                            "Price: %{y:.2f} USD/bbl<extra></extra>"
                    )
                )

            y_title = "Oil Price (USD / barrel)"

        else:  # GAS
            df = query("""
                SELECT date, price
                FROM price
                WHERE benchmark = 'Henry Hub'
                ORDER BY date
            """)

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=df["date"],
                    y=df["price"],
                    name="Henry Hub",
                    mode="lines",
                    line=dict(width=2.5, color="#72B7B2"),
                    hovertemplate=
                        "<b>Henry Hub</b><br>" +
                        "Date: %{x|%Y-%m-%d}<br>" +
                        "Price: %{y:.2f} USD/MMBtu<extra></extra>"
                )
            )

            y_title = "Gas Price (USD / MMBtu)"

        fig.update_layout(
            height=420,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117",
            font=dict(color="#EDEDED"),
            hovermode="x unified",

            legend=dict(
                title="Click to focus / hide",
                bgcolor="rgba(0,0,0,0)"
            ),

            xaxis=dict(
                title="Date",
                showgrid=False
            ),

            yaxis=dict(
                title=y_title,
                showgrid=True,
                gridcolor="rgba(255,255,255,0.08)",
                range=[0, 160] 
            )
        )

        return fig
    
    @app.callback(
        Output("oil-kpi", "children"),
        Output("gas-kpi", "children"),
        Output("facilities-kpi", "children"),
        Input("commodity-selector", "value")
    )
    def update_kpis(_):

        oil = query("""
            SELECT SUM(Production) AS v
            FROM oil_prod
            WHERE Year = (SELECT MAX(Year) FROM oil_prod)
        """)["v"][0]

        gas = query("""
            SELECT SUM(Production) AS v
            FROM gas_prod
            WHERE Year = (SELECT MAX(Year) FROM gas_prod)
        """)["v"][0]

        facilities = query("""
            SELECT COUNT(*) AS v
            FROM ogim
        """)["v"][0]

        return f"{oil:,.0f}", f"{gas:,.0f}", f"{facilities:,}"
