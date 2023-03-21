import dash
from dash import html, dcc 
from dash import callback_context
from dash.dependencies import Input, Output, State

# This will be the home page
dash.register_page(__name__, path='/')

layout = html.Div(
    [
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
                                html.Form(
                                    action="index.html",
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
                                                # html.Label(
                                                #     id="textarea_label",
                                                #     children='Type your question here',
                                                #     htmlFor=""
                                                # )
                                            ]
                                        ),
                                        html.Button(
                                            'Search',
                                            className="formBtn",
                                            type="submit"
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
                                                                html.H4('Detected Tags')
                                                            ]
                                                        ),
                                                        html.Div(
                                                            className="recommendUsers",
                                                            children=[
                                                                html.H4('Recommended Engineers')
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