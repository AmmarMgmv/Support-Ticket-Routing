import dash
from dash import html, dcc 
import plotly.express as px
from dash import html, dcc, dash_table, callback_context
from apps import navigation, dataManipulator, dataReader
import main

tagsDF = dataReader.questionsPerTag(main.tagDataset)
QsPerMonthYear = dataReader.questionsPerMonthAndYear(main.tagDataset, main.aDataset)
QsPerDay = dataReader.questionsPerDay(main.qDataset)
sortedTopScoreOwners = dataReader.topOwnerIdTag(main.tagDataset, main.aDataset)

fig = px.bar(tagsDF.head(20), x='Tag', y='Occurrences', barmode="group")                 # barchart showing most searched tags
fig2 = px.scatter(QsPerMonthYear, x='Date', y='Count')                                   # scatter graph showing year-month and no. of questions
fig3 = px.bar(QsPerDay, x='Date', y='QsAsked', barmode="group")                          # barchart showing date and no. of questions
# pieC = px.pie(AllQsQueries, values=None, names='Tag', 
#              title='Unanswered and Answered Questions per Tag', 
#              hover_data={'QuestionsAsked':True, 'QuestionsUnans':True, 'QuestionsAns':True},
#              labels={'QuestionsUnans':'Unanswered', 'QuestionsAns':'Answered'})

analytics_layout = html.Div(children=[
    navigation.navbar,
    html.Div(
        className="infoRow",
        children=[
            html.Div(
                className="infoTab",
                children=[
                    '1,048,576 Questions'
                ]
            ),
            html.Div(
                className="infoTab",
                children=[
                    '1,048,576 Answers'
                ]
            ),
            html.Div(
                className="infoTab",
                children=[
                    '3,750,995 Different Tags'
                ]
            ),
            html.Div(
                className="infoTab",
                children=[
                    '467,798 Unique Users'
                ]
            ),
        ]
    ),
    html.Div(
        className="doubleRow",
        children=[
            html.Div(
                className="occurrenceColumn",
                children=[
                    html.Div(
                        className="ocurrenceRow",
                        children=[
                            html.H1(
                                className="occurrenceTitle",
                                children='Top 20 Most Searched Tags',
                            ),
                            dcc.Graph(
                                id='tag-graph',
                                figure=fig
                            ),
                        ]
                    ),
                ]
            ),
            html.Div(
                className="yearColumn",
                children=[
                    html.Div(
                        className="yearMonthRow",
                        children=[
                            html.H1(
                                className="MYTitle",
                                children='Number of Tags Searched per Month/Year',
                            ),
                            dcc.Graph(
                                id='MY-graph',
                                figure=fig2
                            ),
                        ]
                    )
                ]
            ),
        ]
    ),
    html.Div(
        className="singleRow",
        children=[
            html.H1(
                className="QuestionNoTitle",
                children=['Number of Questions per Day'],
            ),
            dcc.Graph(
                id='questions-graph',
                figure=fig3
            ), 
        ]
    ),
    html.Div(
        className="tableRow",
        children=[
            html.H1(
                className="smallTableTitle",
                children=['Tags and Their Frequency']
            ),
            html.Div(
                className="smallTableCol",
                children=[
                    html.Div(
                        dash_table.DataTable(
                            tagsDF.to_dict('records'),
                            columns=[
                                {'name': 'Tag', 'id': 'Tag'},
                                {'name': 'Frequency', 'id': 'Occurrences'},
                            ],
                            style_cell_conditional=[
                                {
                                    'textAlign': 'left',
                                }
                            ],
                            filter_action='native',
                            page_size=14,
                            style_table={
                                'height': '800px',
                                'overflowY': 'auto',
                            },
                            fixed_rows={'headers': True},
                            style_header={
                                'backgroundColor': '#054b80',
                                'fontWeight':'bold',
                                'color': 'white',
                            },
                            style_data={
                                'overflow': 'hidden',
                                'textOverflow': 'ellipsis',
                                'width':'50%'
                            },
                        ),
                    ),
                ]
            ),
            # html.Div(
            #     className="pieChart",
            #     children=[
            #         # dcc.Dropdown(
            #         #     id="dropdown",
            #         #     options=[{"label": tag, "value": tag} for tag in AllQsQueries["Tag"].unique()],
            #         #     value=AllQsQueries["Tag"].unique()[0]
            #         # ),
            #         # dcc.Graph(id="pie-chart"),
            #     ]
            # )    
        ]
    ),
    html.H1(
        className="bigTableTitle",
        children=['Top Scoring ID for Each Tag']
    ),
    html.Div(
        className="bigTable",
        children=[
            html.Div(
                dash_table.DataTable(
                    sortedTopScoreOwners.to_dict('records'),
                    columns=[
                        {'name': 'Issue', 'id': 'Tag'},
                        {'name': 'ID no. of staff member', 'id': 'OwnerUserId'},
                        {'name': 'Score', 'id': 'Score'},
                    ],
                    style_cell_conditional=[
                        {
                            'textAlign': 'left',
                        }
                    ],
                    filter_action='native',
                    page_size=14,
                    fixed_rows={'headers': True},
                    style_header={
                        'backgroundColor': '#054b80',
                        'color': 'white',
                    },
                    style_data={
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        'width':'33.3%'
                    },
                )
            )
        ]
     ), 
])

# @app.callback(
#     dash.dependencies.Output("pie-chart", "figure"),
#     [dash.dependencies.Input("dropdown", "value")]
# )
# def update_pie_chart(tag):
#     # Filter the AllQsQueries DataFrame by the selected tag
#     data = AllQsQueries[AllQsQueries["Tag"] == tag]

#     # Check if there are any unanswered or answered questions for this tag
#     if data["QuestionsAns"].iloc[0] == 0 and data["QuestionsUnans"].iloc[0] == 0:
#         pieC = px.pie(names=["No Data"], values=[1])
#         pieC.update_layout(title=f"No Answered or Unanswered Questions for {tag} Tag")
#     else:
#         values = []
#         names = []
#         if data["QuestionsAns"].iloc[0] > 0:
#             values.append(data["QuestionsAns"].iloc[0])
#             names.append("Answered")
#         if data["QuestionsUnans"].iloc[0] > 0:
#             values.append(data["QuestionsUnans"].iloc[0])
#             names.append("Unanswered")
#         pieC = px.pie(values=values, names=names, hole=.3)
#         pieC.update_layout(title=f"Answered and Unanswered Questions for {tag} Tag")

#     return pieC