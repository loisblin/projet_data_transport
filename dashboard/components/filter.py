from dash import html, dcc

def create_filters(state_filter, state_time):

    city = state_filter.get("city")
    day = state_time.get("day")
    hour = state_time.get("hour")
    f = format_selection(city, day, hour)

    map_metric = state_filter.get("map_metric")
    histo_metric = state_filter.get("histo_metric")

    return html.Div([

        html.Div(
            f,
            id="filter-title",
            style={"color": "#bbb", "marginBottom": "10px"}
        ),

        html.Hr(style={"borderColor": "#333"}),

        metric_toggle("Histogram", "histo-metric-toggle", histo_metric),
        metric_toggle("Map", "map-metric-toggle", map_metric),
    ])


def format_selection(city, day, hour):
    f = ""
    if city is not None:
        f = f + f"City: {city}"
    if day is not None:
        if city is not None:
            f = f + "    |"
        f = f + f"Day: {day}"
        if hour is not None:
            f = f + f"  |Hour: {hour}h"
    if city is None and day is None:
        f = "No filter Activated  "
    return f


def toggle_class(value):
    return f"toggle-wrapper {'toggle-price' if value == 'price' else 'toggle-delay'}"


def metric_toggle(label, component_id, value="price"):
    return html.Div([

        html.Span(
            label,
            style={
                "color": "white",
                "marginRight": "12px",
                "minWidth": "90px"
            }
        ),

        html.Div(
            [
                html.Div("Price", className="toggle-option"),
                html.Div("Delay", className="toggle-option"),
                html.Div(className="toggle-slider"),
            ],
            id=component_id,
            n_clicks=0,
            className=toggle_class(value)
        )

    ], style={
        "display": "flex",
        "alignItems": "center",
        "gap": "10px"
    })