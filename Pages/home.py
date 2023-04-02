import dash
from dash import html, dcc 
from dash import callback_context
from dash.dependencies import Input, Output, State
from apps import navigation
from main import app
import main
from apps import dataManipulator

home_layout = html.Div(children=
    [
        navigation.navbar,
        html.Div(
            className="indexContainer",
            children=[
                html.Span(className="big-circle"),
                html.Span(className="big-circle-left"),
                html.Div(
                    className="indexForm",
                    children=[
                        html.Div(
                            className="contact-info",
                            children=[
                                html.H2(
                                    'Welcome to Millennium Management', 
                                    className="indexTitle"
                                ),
                                html.P(
                                    'Millennium is a global investment management firm, built on a sophisticated '
                                    'operating system at scale. We seek to pursue a diverse array of investment strategies,'
                                    ' and we empower our employees to deliver exceptional outcomes and enable our portfolio '
                                    'managers to do what they do best, navigate the markets.', 
                                    className="infoText"
                                ),
                                html.Div(
                                    className="logo",
                                    children=[
                                        html.Img(src='https://largest.org/wp-content/uploads/2019/01/Millennium-Management.png')
                                    ]
                                ),
                                html.H2(
                                    'Have a question you need help with?', 
                                    className="indexTitle"
                                ),
                                html.P(
                                    'Input your question into the form on the right and our program will detect what tags it '
                                    'belongs to and suggest support engineers that may be able to answer your question based on '
                                    'these tags as well as the engineers expertise and past experience.', 
                                    className="infoText"
                                )
                            ]
                        ),
                        html.Div(
                            className="contact-form",
                            children=[
                                html.Span(className="circle one"),
                                html.Span(className="circle two"),
                                html.Div(
                                    # action="index.html",
                                    className="formDiv",
                                    children=[
                                        html.H3(
                                            'Need Help?',
                                            className="indexTitle"
                                        ),
                                        html.Div(
                                            className="input-container textarea",
                                            children=[
                                                dcc.Textarea(
                                                    id="question_textarea",
                                                    className="indexInput",
                                                    placeholder='Type your question here'
                                                ),
                                            ]
                                        ),
                                        html.Button(
                                            'Search',
                                            className="formBtn",
                                            type="submit",
                                            id="searchButton",
                                            n_clicks=0
                                        ),
                                        html.Div(
                                            className="resultContainer",
                                            children=[
                                                html.Div(
                                                    className="resultForm",
                                                    children=[
                                                        html.Div(
                                                            className="detectedTags",
                                                            children=[
                                                                html.H4('Detected Tags'),
                                                                html.Div(
                                                                    id="dTags",
                                                                    className="printedTags"
                                                                )
                                                            ]
                                                        ),
                                                        html.Div(
                                                            className="recommendUsers",
                                                            children=[
                                                                html.H4('Recommended Engineers'),
                                                                html.Div(
                                                                    id="engineers",
                                                                    className="printedEngineers"
                                                                )
                                                            ]
                                                        ),
                                                    ]
                                                ),
                                            ]
                                        ),
                                    ]
                                )
                            ]
                        )
                    ]
                ),
            ]
        ), 
    ],
)
def ranker(engineersList):
    sorted_engineers = sorted(engineersList, key=lambda x: x["Score"], reverse=True)

    return sorted_engineers[:5]

#Callback for getting the engineers best suited to the question
# @app.callback(
#     # Output(component_id='dTags', component_property='children'),
#      Output(component_id='engineers', component_property='children'),
#     [Input(component_id='question_textarea', component_property='value')],
#     prevent_initial_call=True
# )
# def updateInfo(n,input):
#     engineer=[]
#     engineer_div = html.Div([])
    
#     engineer = main.index_search("index_dir", ["Body"], input)
#     topEngineers = ranker(engineer)

#     engineersDivs = []
#     for i, row in topEngineers.iterrows():
#         div = html.Div(
#         className="userCard",
#         children=[
#             html.P(f"ID: {row['Ids']}"),
#             html.P(f"Name: {row['FirstName']} {row['LastName']}"),
#             html.P(f"Email: {row['Email']}"),
#             html.P(f"Job Title: {row['JobTitle']}"),
#             html.P(f"Address: {row['Address']}"),
#             html.P(f"Status: {row['Status']}"),
#         ])
#         engineersDivs.append(div)

#     if n > 0 and input != "":
#         engineer_div = html.Div([
#             *[html.Div(e, className="eachEngineer") for e in engineer]
#         ])
#     return engineer_div

#Callback for getting the tags associated with the question
@app.callback(
    Output(component_id='dTags', component_property='children'),
    [Input(component_id='question_textarea', component_property='value')],
    prevent_initial_call=True
)
def updateInfo(input):

    tag = dataManipulator.detectTagsFromInput(main.overlap_words, input)
    # Create a div for tags
    tag_div = html.Div([
        *[html.Div(t, className="eachTag") for t in tag]
    ])
    return tag_div