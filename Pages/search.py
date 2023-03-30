import dash
from dash import html, dcc 
import plotly.express as px
from dash.dependencies import Input, Output, State
from apps import navigation
from main import *

def testfunc(input):
    if input != "":
        question = "This is the " + input + " question"
        answer = "This is the " + input + " answer"
        return question, answer

search_layout = html.Div(children=
    [
        navigation.navbar,
        html.Div(
            className="searchContainer",
            children=[
                html.Div(
                    # action="{{ url_for('search') }}",
                    # method="POST",
                    className="search-bar",
                    children=[
                        dcc.Input(
                            placeholder="Search through previously asked questions...",
                            type="text",
                            value="",
                            # name="search-input",
                            id="userInput"
                        ),
                        html.Button(
                            type="Search",
                            children=[
                                html.Img(
                                    src="https://img.icons8.com/ios/256/search.png"
                                )
                            ],
                            n_clicks=0,
                            id="mybutton"
                        )
                    ]
                ),
                html.Div(
                    className="searchForm",
                    children=[
                        html.Div(
                            id='presults',
                            style={'overflow': 'auto', 'height': '100%', 'padding':'2rem'}
                        ),
                    ],
                )
            ]
        ), 
    ],
)
