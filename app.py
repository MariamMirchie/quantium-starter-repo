import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

DATA_PATH = "data/pink_morsels_sales.csv"
PRICE_INCREASE_DATE = "2021-01-15"

def load_data():
    df = pd.read_csv(DATA_PATH)


    expected = {"Sales", "Date", "Region"}
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in {DATA_PATH}: {sorted(missing)}")

    df["Date"] = pd.to_datetime(df["Date"])
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce").fillna(0)

    return df

df = load_data()


regions = sorted(df["Region"].dropna().unique().tolist())
region_options = [{"label": "All Regions", "value": "ALL"}] + [
    {"label": r, "value": r} for r in regions
]

app = Dash(__name__)

app.layout = html.Div(
    style={"maxWidth": "1100px", "margin": "0 auto", "padding": "24px"},
    children=[
        html.H1("Pink Morsels Sales Visualiser"),

        html.P(
            "Line chart of Pink Morsels sales over time. "
            "The price increase occurred on Jan 15, 2021."
        ),

        html.Label("Region"),
        dcc.Dropdown(
            id="region",
            options=region_options,
            value="ALL",
            clearable=False,
            style={"marginBottom": "16px"},
        ),

        dcc.Graph(id="sales-line"),
    ],
)

@app.callback(
    Output("sales-line", "figure"),
    Input("region", "value"),
)
def update_chart(region_value):
    dff = df.copy()
    if region_value != "ALL":
        dff = dff[dff["Region"] == region_value]

   
    daily = (
        dff.groupby("Date", as_index=False)["Sales"]
        .sum()
        .sort_values("Date")
    )

    fig = px.line(
        daily,
        x="Date",
        y="Sales",
        title="Daily Sales (Pink Morsels)",
        labels={"Date": "Date", "Sales": "Sales ($)"},
    )

   
    fig.add_vline(
        x=pd.to_datetime(PRICE_INCREASE_DATE),
        line_width=2,
        line_dash="dash",
        line_color="red",
    )
    fig.add_annotation(
        x=pd.to_datetime(PRICE_INCREASE_DATE),
        y=daily["Sales"].max() if len(daily) else 0,
        text="Price increase (2021-01-15)",
        showarrow=True,
        arrowhead=2,
        yanchor="bottom",
    )

    fig.update_layout(margin=dict(l=40, r=20, t=60, b=40))
    return fig

if __name__ == "__main__":
    app.run(debug=True)