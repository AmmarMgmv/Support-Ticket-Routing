import dash
from dash import html, dcc 
import plotly.express as px
from apps import navigation

admin_layout = html.Div(
    [
        navigation.navbar,
        html.Br(),
        html.Br(),
        html.Div("welcome to admin"),
    ]
)