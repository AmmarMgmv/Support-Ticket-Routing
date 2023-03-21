import dash
from dash import html, dcc 
from dash import callback_context
from dash.dependencies import Input, Output, State

from main import app
from Pages import admin, analytics, home, search

url_content_layout = html.Div(children=[
        dcc.Location(id="url", refresh=False),
        html.Div(id="output-div")
    ]
)

app.layout = url_content_layout

app.validation_layout = html.Div([
        url_content_layout,
        home.home_layout,
        search.search_layout,
        admin.admin_layout,
        analytics.analytics_layout
    ]
)

@app.callback(Output(component_id="output-div", component_property="children"), Input(component_id="url", component_property="pathname"))
def update_output_div(pathname):
    print(pathname)
    if pathname == "/search":
        return search.search_layout
    elif pathname == "/admin":
        return admin.admin_layout
    elif pathname == "/analytics":
        return analytics.analytics_layout
    else:
        return home.home_layout

if __name__ == '__main__':
    app.run_server(debug=True)