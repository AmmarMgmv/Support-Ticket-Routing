import dash
from dash import html, dcc 
from dash import callback_context
from dash.dependencies import Input, Output, State
from apps import navigation, dataManipulator
from main import app
import main

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
def findTop25(engineers):
    qCounter = 0
    aCounter = 0
    lastQuestion = ""
    top25 = []
    for engineer in engineers:
        # printable_userID = engineer['Ids']
        # printable_Fn = engineer['FirstName']
        # printable_Ln = engineer['LastName']
        # fullID = printable_Fn + " " + printable_Ln + " (" + printable_userID + ")"
        # print(engineer)
        if(lastQuestion != engineer['QuestionBody']):
            aCounter = 0
            qCounter += 1
            if aCounter < 5:
                top25.append(engineer)
                # print(fullID)
                aCounter += 1
        else:
            if aCounter < 5:
                top25.append(engineer)
                # print(fullID)
                aCounter += 1
        lastQuestion = engineer['QuestionBody']
        if qCounter == 5:
                break
    return top25

def findTop5(uniqueE):
    topEngineers = []
    allScores = []
    for engineer in uniqueE:
        allScores.append(engineer['Score'])
    # scores = list(map(int, allScores))
    scores = sorted(allScores, reverse=True)
    top5 = scores[:5]

    engineerCounter = 0
    for engineer in uniqueE:
        userScore = engineer['Score']
        for i in top5:
            if engineerCounter <= 5:
                if i == userScore:
                    topEngineers.append(engineer)
                    engineerCounter += 1
                    break
            else:
                return topEngineers
    return topEngineers

def checkStatus(engineers):
    activeEngineers = []
    for engineer in engineers:
        userId = float(engineer['Ids'])
        if userId not in main.busy_users:
            activeEngineers.append(engineer)     
    return activeEngineers

#Callback for getting the engineers best suited to the question
@app.callback(
    Output(component_id='engineers', component_property='children'),
    [Input(component_id='searchButton', component_property='n_clicks')],
    [State(component_id='question_textarea', component_property='value')],
    prevent_initial_call=True
)
def updateEngineers(n,input):
    engineer=[]
    
    engineer = main.index_search("index_dir", ["Body"], input)
    topEngineers = findTop25(engineer)
    uniqueEngineers = list({v['Ids']:v for v in topEngineers}.values())
    activeEngineers = checkStatus(uniqueEngineers)
    topFive = findTop5(activeEngineers)
    engineersDivs = []
    for i in topFive:
        div = html.Div(
            className="testCard",
            children=[
                html.Div(className="eachEngineer", children=[f"{i['FirstName']} {i['LastName']} (ID: {i['Ids']})"]),
            ])
        engineersDivs.append(div)

    return engineersDivs

#Callback for getting the tags associated with the question
@app.callback(
    Output(component_id='dTags', component_property='children'),
    [Input(component_id='question_textarea', component_property='value')],
    prevent_initial_call=True
)
def updateTags(input):

    input = input.lower()
    input = input.replace('?', '')
    tag = dataManipulator.detectTagsFromInput(main.overlap_words, input)
    # Create a div for tags
    tag_div = html.Div([
        *[html.Div(t, className="eachTag") for t in tag]
    ])
    return tag_div