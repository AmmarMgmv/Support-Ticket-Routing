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
                html.Img(
                    className="hexagon1",
                    src="assets\hexagons.png"
                ),
                # html.Img(
                #     className="dots",
                #     src="assets\dots.png"
                # ),
                html.Div(
                    className="hexagonContainer",
                    children=[
                        html.Img(
                            className="hexagon2",
                            src="assets\hexagons.png"
                        ),
                    ] 
                ),
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
                            className="presults",
                            style={'overflow': 'auto', 'height': '100%', 'padding':'2rem'}
                        ),
                    ],
                )
            ]
        ), 
    ],
)
    
@app.callback(
    Output(component_id='presults', component_property='children'),
    [Input(component_id='mybutton', component_property='n_clicks')],
    [State(component_id='userInput', component_property='value')],
    prevent_initial_call=False
)
def get_results(n, input_question):
    input_question = input_question.replace('?', '')
    printresults = []
    lastQuestion = ""
    qCounter = 0
    aCounter = 0
    if input_question != "":
        results = index_search("index_dir", ["Body"], input_question)
        for result in results:
            printable_userID = result['Ids']
            printable_Fn = result['FirstName']
            printable_Ln = result['LastName']
            fullID = printable_Fn + " " + printable_Ln + " (" + printable_userID + ")"
            printable_q = result['QuestionBody']
            printable_a = result['AnswerBody']
            if (lastQuestion != result['QuestionBody']):
                aCounter = 0
                qCounter += 1
                if aCounter < 5:
                    printresults.append(html.Div(
                    [
                        html.Div(printable_q, className="searchQuestion"),
                        html.Div([
                            html.Div(fullID, className="usersID"), html.Div(printable_a, className="usersAnswer")], className="searchAnswer")
                    ],
                    className="eachResult"
                    ))
                    aCounter += 1
            else:
                if aCounter < 5:
                    printresults[-1].children.append(html.Div(
                        [html.Div(fullID, className="usersID" ), html.Div(printable_a, className="usersAnswer")], className="searchAnswer"))
                    aCounter += 1
            lastQuestion = result['QuestionBody']
            if qCounter == 5:
                break
        return printresults  
    else:
        return []