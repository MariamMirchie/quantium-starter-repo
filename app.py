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

    # Normalize region values for the radio options required by the task
    df["Region"] = df["Region"].astype(str).str.strip().str.lower()

    return df

df = load_data()

REGION_OPTIONS = [
    {"label": "North", "value": "north"},
    {"label": "East", "value": "east"},
    {"label": "South", "value": "south"},
    {"label": "West", "value": "west"},
    {"label": "All", "value": "all"},
]

app = Dash(__name__)
app.title = "Pink Morsels Sales"

app.layout = html.Div(
    className="container",
    children=[
        html.Div(
            className="header",
            children=[
                html.H1("Pink Morsels Sales Visualiser", className="title"),
                html.P(
                    "Explore Pink Morsels sales over time by region. "
                    "The price increase occurred on 2021-01-15 (shown as a dashed red line).",
                    className="subtitle",
                ),
            ],
        ),

        html.Div(
            className="card",
            children=[
                html.Div(
                    className="controls",
                    children=[
                        html.Div("Filter by region", className="label"),
                        dcc.RadioItems(
                            id="region-radio",
                            options=REGION_OPTIONS,
                            value="all",
                            className="radio-wrap",
                            inline=True,
                        ),
                    ],
                ),

                dcc.Graph(id="sales-line"),
            ],
        ),
    ],
)

@app.callback(
    Output("sales-line", "figure"),
    Input("region-radio", "value"),
)
def update_chart(region_value):
    dff = df.copy()
    if region_value != "all":
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

    # Make the chart match the dark theme a bit better
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e8ecff",
        title_font_color="#e8ecff",
        margin=dict(l=50, r=20, t=60, b=45),
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.08)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.08)")

    return fig

if __name__ == "__main__":
    app.run(debug=True)