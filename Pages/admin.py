import dash
from dash import html, dcc 
import plotly.express as px

dash.register_page(__name__)

layout = html.Div(
    [
    dcc.Markdown('# This will be the content of the admin page')
    ]
)