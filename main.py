import dash
import pandas as pd
import spacy
from lxml.html import fromstring
import re
from apps import dataManipulator, dataReader
import numpy as np
from itertools import product
from dash import html, dcc, dash_table, callback_context
import dash_table_experiments as dt
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
import dash_bootstrap_components as dbc
from  previous_similar_answers import get_body
# ------------------------------------------------------------------------------------------
# 
#                               LOAD IN THE DATASETS                               
# 
# ------------------------------------------------------------------------------------------

# Import the datasets (changed encoding as default is utf-8, which
# does not support some characters in the datasets
tagDataset = pd.read_csv("Dataset\Tags.csv", encoding = "ISO-8859-1")
qDataset = pd.read_csv("Dataset\Questions.csv", encoding = "ISO-8859-1")
aDataset = pd.read_csv("Dataset\Answers.csv", encoding = "ISO-8859-1")

# ## FOR DEBUG: temporarily reads the first 200 rows of csv files
# tagDataset = pd.read_csv("Dataset\Tags.csv", nrows = 2, encoding = "ISO-8859-1")
# qDataset = pd.read_csv("Dataset\Questions.csv", nrows = 5, encoding = "ISO-8859-1")
# aDataset = pd.read_csv("Dataset\Answers.csv", nrows = 5, encoding = "ISO-8859-1")

# ------------------------------------------------------------------------------------------
# 
#                               CLEAN OR LOAD CLEANED DATASET                               
# 
# ------------------------------------------------------------------------------------------

# Load the cleaned CSV file (if it exists)
# try:
#     qDataset = pd.read_csv("Dataset/Questions_cleanLemma.csv")
#     print("Cleaned dataset loaded from file")
# except FileNotFoundError:
# # If the cleaned CSV file does not exist, then clean the dataset and save it to file
#     print("Cleaning dataset...")
#     qDataset['Cleaned Body'] = qDataset['Body'].apply(remove_tags)
#     qDataset['Cleaned Title'] = cleanAndLemmatize(qDataset, 'Title')
#     qDataset['Cleaned Body'] = cleanAndLemmatize(qDataset, 'Cleaned Body')
#     qDataset['Title'] = qDataset['Cleaned Title']
#     qDataset['Body'] = qDataset['Cleaned Body']
#     qDataset.drop('Cleaned Title', axis=1, inplace=True)
#     qDataset.drop('Cleaned Body', axis=1, inplace=True)
#     qDataset.to_csv("Dataset/Questions_cleanLemma.csv", index=False)
#     print("Cleaned dataset saved to file")

# TagsQs = pd.merge(tagDataset, qDataset[["Id", "Title", "Body"]], on="Id")
# groups = TagsQs.groupby('Tag')

# ------------------------------------------------------------------------------------------
# 
#                                  FUZZY SEARCH ALGORITHM                               
# 
# ------------------------------------------------------------------------------------------

# def remove_html_tags(text):
#     clean = re.compile('<.*?>')
#     return re.sub(clean, '', text)
    
# # fuzzy search on question data set
# from whoosh.fields import Schema, TEXT, ID
# from whoosh import index, qparser
# from whoosh.analysis import RegexTokenizer, LowercaseFilter
# from whoosh.writing import BufferedWriter
# from whoosh.qparser import FuzzyTermPlugin
# import os

# my_analyzer = RegexTokenizer() | LowercaseFilter()

# # Define the schema for the index
# schema = Schema(Body=TEXT(stored=True, analyzer=my_analyzer))

# # Create the index directory if it doesn't exist
# if not os.path.exists("index_dir"):
#     os.mkdir("index_dir")

# # Create the index and add documents to it
# ix = index.create_in("index_dir", schema)
# writer= ix.writer()

# for i, row in qDataset.iterrows():
#     Body = remove_html_tags (row ["Body"])
#     ##answerBody = remove_html_tags(row["answerBody"])
#     writer.add_document(Body=Body)
#     if i == 10000:
#         break
# writer.commit()

# # Function to search the index
# def index_search(search_fields, search_query):
#     ix = index.open_dir("index_dir")
#     schema = ix.schema
    
#     og = qparser.OrGroup.factory(0.8)
#     mp = qparser.MultifieldParser(search_fields, schema, group=og)
#     mp.add_plugin(FuzzyTermPlugin())
#     q = mp.parse(search_query + "~")
    
#     with ix.searcher() as searcher:
#         results = searcher.search(q, limit=5)
        
#         # Build a dictionary of search results
#         results_dict = {}
#         for hit in results:
#             results_dict[hit.fields()["Body"]] = hit.score
            
#         return results_dict


#Prompt the user for search queries
# while True:
#     query = input("Enter your query (or 0 to exit): ")
#     if query == "0":
#         break
#     else:
#         results = index_search("index_dir", ["Body"], query)
#         print("Search results:")
#         for i, result in enumerate(results, start=1):
#          print(f"{i}. {result}\n")

# ------------------------------------------------------------------------------------------
# 
#                            FIND OVERLAPPING WORDS & DETECT TAGS                               
# 
# ------------------------------------------------------------------------------------------

# tag_common, all_common_words = commonWords(groups)
# overlap_words = overlappedCommonWords(tag_common, all_common_words)
# detectTags(qDataset, overlap_words)

# ------------------------------------------------------------------------------------------
# 
#                            CREATE DASH APP WITH GRAPHS/TABLES                               
# 
# ------------------------------------------------------------------------------------------

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR])
server = app.server

sortedTags = tagDataset.groupby(["Tag"]).size() #count how many in each "group: "Tag" 
sortByTop = sortedTags.sort_values(ascending=False) #sort to show top categories
df_tag = pd.DataFrame({'Tag': sortByTop.index, 'Occurrences': sortByTop.values})
df_tag.head(15)

TagsAnswers = pd.merge(tagDataset, aDataset, left_on='Id', right_on='ParentId')
summedScore = TagsAnswers.groupby(['Tag', 'OwnerUserId'])['Score'].sum().reset_index()
topScoreOwners = summedScore.groupby('Tag').agg({'Score': 'idxmax'}).reset_index()
topScoreOwners = summedScore.iloc[topScoreOwners['Score']]
sortedTopScoreOwners = topScoreOwners.sort_values('Score', ascending=False)
df=sortedTopScoreOwners

# filters = html.Div(children=[
#     html.H1(children='Graph showing the top 20 most searched tags',style={'textAlign': 'center','font-family':'Arial'}),
#     dcc.Graph(
#         id='tag-graph',
#         figure=fig
#     ),
#     html.H1(children='Table showing tags and frequency',style={'textAlign': 'center','font-family':'Arial'}),
#     html.Div(dash_table.DataTable(
#         tagsDF.to_dict('records'),
#         columns=[
#             {'name': 'Tag', 'id': 'Tag'},
#             {'name': 'Frequency', 'id': 'Occurrences'},
#         ],
#         filter_action='native',
#         page_size=20,
#         fixed_rows={'headers': True},
#         style_header={
#             'backgroundColor': 'rgb(30, 30, 30)',
#             'color': 'white',
#         },
#         style_data={
#             'overflow': 'hidden',
#             'textOverflow': 'ellipsis',
#         },
#     )),
#     html.H1(children='Graph showing questions asked by month and year',style={'textAlign': 'center','font-family':'Arial'}),
#     dcc.Graph(
#         id='MY-graph',
#         figure=fig2
#     ),
#     html.H1(children='Graph showing the number of questions per day',style={'textAlign': 'center','font-family':'Arial'}),
#     dcc.Graph(
#         id='questions-graph',
#         figure=fig3
#     ),
#     html.H1(children='Table showing top ID for each tag',
#             style={
#                 'textAlign': 'center',
#                 'font-family' : 'Arial'
#             }),
#     html.Div(dash_table.DataTable(
#         sortedTopScoreOwners.to_dict('records'),
#         columns=[
#             {'name': 'Issue', 'id': 'Tag'},
#             {'name': 'ID no. of staff member', 'id': 'OwnerUserId'},
#             {'name': 'Score', 'id': 'Score'},
#         ],
#         filter_action='native',
#         page_size=20,
#         fixed_rows={'headers': True},
#         style_header={
#                 'backgroundColor': 'rgb(30, 30, 30)',
#                 'color': 'white',
#             },
#         style_data={
#             'overflow': 'hidden',
#             'textOverflow': 'ellipsis',
#         },
#         ))
# ])

# app.layout = html.Div(children=[filters])

# if __name__ == '__main__':
#     app.run_server(debug=True)

app = Dash(__name__)
app.config.suppress_callback_exceptions = True
app.title="Medal_dashboard"
previous_list={}

styles = {
'nav-link': {
    'textDecoration': 'none',
    'color': 'white',
    'padding': '5px'
    },
    'nav-link:hover': {
    'textDecoration': 'underline',
    'cursor': 'pointer'
    }
}
    
home_layout = html.Div([
    html.Nav([
         html.Ul([
            html.Li(html.A('Home', href='/', style=styles['nav-link'])),
            html.Li(html.A('Search', href='/search', style=styles['nav-link'])),
            html.Li(html.A('Admin', href='/admin', style=styles['nav-link'])),
            html.Li(html.A('Analytics',href='/analysis',style=styles['nav-link'])),
            html.Li("Millennium management",style={'color':'white'})
        ], style={'display': 'flex', 'list-style': 'none', 'margin': 0, 'padding': 0,'gap': '40px'})
    ], style={'background-color': 'rgb(51,105,192)', 'padding': '10px','border-radius':'10px'}),

    html.Div([
        html.Div("Welcome to Millennium management", style={'color': 'white', 'text-align': 'center', 'padding-top': '40px','font-size':'30px'}),
        html.Div("Have a question?",style={'color':'white','text-align': 'center','padding-top': '40px','font-size':'30px'}),
        html.Div("Ask down below",style={'color':'white','text-align': 'center','padding-top': '40px','font-size':'30px'}),
    ],style={'background-color': 'rgb(173, 216, 230)', 'height': '350px', 'width': '100%','border-radius':'10px'}),
    
    html.Div([
        dcc.Input(
            id='search-input',
            type='text',
            placeholder='Ask a question',
            style={'width':'60%','border-radius':'10px','height':'50px','border':'1px solid white','margin-left':'10%','margin-top':'20px','background-color':'#f2f2f2','font-size':'25px'}
        ),

        html.Button('Search', id='search-button',style={'font-size':'25px','margin-left':'50px','border-radius':'10px','border':'1px solid white'}),
    ],style={'background-color':'rgb(59, 140, 225)','width':'90%','height':'350px','margin-left':'80px','margin-top':'30px','border-radius':'10px'}),
        

    html.Div(id='search-output')
])
    




admin_layout=html.Div([


])
analysis_layout=html.Div([
    html.Nav([
         html.Ul([
            html.Li(html.A('Home', href='/', style=styles['nav-link'])),
            html.Li(html.A('Search', href='/search', style=styles['nav-link'])),
            html.Li(html.A('Admin', href='/admin', style=styles['nav-link'])),
            html.Li(html.A('Analytics',href='/analysis',style=styles['nav-link'])),
            html.Li("Millennium management",style={'color':'white'})
        ], style={'display': 'flex', 'list-style': 'none', 'margin': 0, 'padding': 0,'gap': '40px'})
    ], style={'background-color': 'rgb(51,105,192)', 'padding': '10px'}),

    html.Div(
    'Analytics',style={"background-color":'rgb(173, 216, 230)','padding':'0px','width':'100%','height':'100px','font-size':'30px','text-align':'center'}
    ),
           
])
search_layout=html.Div([
    html.Nav([
         html.Ul([
            html.Li(html.A('Home', href='/', style=styles['nav-link'])),
            html.Li(html.A('Search', href='/search', style=styles['nav-link'])),
            html.Li(html.A('Admin', href='/admin', style=styles['nav-link'])),
            html.Li(html.A('Analytics',href='/analysis',style=styles['nav-link'])),
            html.Li("Millennium management",style={'color':'white'})
        ], style={'display': 'flex', 'list-style': 'none', 'margin': 0, 'padding': 0,'gap': '40px'})
    ], style={'background-color': 'rgb(51,105,192)', 'padding': '10px','border-radius':'10px'}),

    html.Div([
        html.Div("Search through previously asked questions", style={'color': 'white', 'text-align': 'center', 'padding-top': '40px','font-size':'30px'}),
        
        html.Div([
        dcc.Input(
            id='search-previous',
            type='text',
            placeholder='Search......',
            style={'width':'60%','border-radius':'10px','height':'50px','border':'1px solid white','margin-left':'10%','margin-top':'20px','background-color':'#f2f2f2','font-size':'25px'}
        ),
        html.Button('Search', id='previous-button',style={'font-size':'25px','margin-left':'50px','border-radius':'10px','border':'1px solid white'}),
    ]),
      

       html.Div([
       "Answers for previous similar questions",

       dash_table.DataTable(
    id='datatable',
    columns=[
        {'name': 'Answers to previous', 'id': 'Values', 'type': 'text', 'presentation': 'markdown'}
    ],
    style_table={
        'height': '500px',
        'overflowY': 'scroll',
        'border': 'thin lightgrey solid'
    },
    style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold',
        'border': 'thin lightgrey solid'
    },
    style_cell={
        'minWidth': '0px',
        'maxWidth': '250px',
        'whiteSpace': 'normal',
        'fontSize': '15px',
        'height': 'auto',
        'textAlign': 'left',
        'border': 'thin lightgrey solid'
    },
    page_size=30,
    page_action='none',
    sort_action='none',
    filter_action='none'
),

       html.Div(id='previous_output')
       ],style={'background-color':'white','width':'90%','border-radius':'10px','height':'50%','margin-left':'5%','margin-top':'5%'},

       ),

        ],style={'background-color': 'rgb(173, 216, 230)', 'height': '1000px', 'width': '100%','border-radius':'10px','font-size':'30px','text-align': 'center'}),
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/search':
        return search_layout
    elif pathname == '/admin':
        return admin_layout
    elif pathname =='/analysis':
        return analysis_layout
    else:
        return home_layout

@app.callback(Output('datatable', 'data'),
              [Input('previous-button', 'n_clicks')],
              [State('search-previous', 'value')])
def previous_search(n_clicks,value):
    if n_clicks is not None:
     previous_list=get_body(value)
     data = [{'Values': val} for val in previous_list]
     return data
    else:
        return []



if __name__ == '__main__':
    app.run_server(debug=True)
