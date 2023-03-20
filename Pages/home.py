import dash
from dash import html, dcc 
import plotly.express as px

# This will be the home page
dash.register_page(__name__, path='/')

layout = html.Div(
    [
    dcc.Markdown('# This will be the content of the home page')
    ]
)