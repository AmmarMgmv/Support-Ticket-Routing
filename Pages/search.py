import dash
from dash import html, dcc 
import plotly.express as px
from apps import navigation

search_layout = html.Div(
    [
        navigation.navbar,
        html.Br(),
        html.Br(),
        html.Div("welcome to search"),
    ]
)

# dash.register_page(__name__)

# layout = html.Div(
#     [
#         dcc.Markdown('# This will be the content of the search page')
#     ]
# )