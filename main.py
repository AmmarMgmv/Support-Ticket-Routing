import dash
import pandas as pd
import spacy
from lxml.html import fromstring
import re
from dataReader import *
from dataManipulator import *
from dash import dash_table
import numpy as np
from itertools import product
import dash
from dash import html
from dash import dcc
from dash import dash_table
import dash_table_experiments as dt
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
from collections import Counter

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
try:
    qDataset = pd.read_csv("Dataset/Questions_cleanLemma.csv")
    print("Cleaned dataset loaded from file")
except FileNotFoundError:
# If the cleaned CSV file does not exist, then clean the dataset and save it to file
    print("Cleaning dataset...")
    qDataset['Cleaned Body'] = qDataset['Body'].apply(remove_tags)
    qDataset['Cleaned Title'] = cleanAndLemmatize(qDataset, 'Title')
    qDataset['Cleaned Body'] = cleanAndLemmatize(qDataset, 'Cleaned Body')
    qDataset['Title'] = qDataset['Cleaned Title']
    qDataset['Body'] = qDataset['Cleaned Body']
    qDataset.drop('Cleaned Title', axis=1, inplace=True)
    qDataset.drop('Cleaned Body', axis=1, inplace=True)
    qDataset.to_csv("Dataset/Questions_cleanLemma.csv", index=False)
    print("Cleaned dataset saved to file")

TagsQs = pd.merge(tagDataset, qDataset[["Id", "Title", "Body"]], on="Id")
groups = TagsQs.groupby('Tag')

# ------------------------------------------------------------------------------------------
# 
#                                  FUZZY SEARCH ALGORITHM                               
# 
# ------------------------------------------------------------------------------------------

# import the package to work on the datasets
import pandas as pd
import spacy
from lxml.html import fromstring
import re

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

#load the datasets 
# specify the columns you want to read
columns_to_read = ['Body', 'Id']
quesDataset = pd.read_csv("Dataset\Questions.csv", encoding = "ISO-8859-1",usecols=columns_to_read)

columns_to_read_answers = ['Body', 'ParentId']
ansDataset = pd.read_csv("Dataset\Answers.csv",encoding = "ISO-8859-1",usecols=columns_to_read_answers)
ansDataset = ansDataset.rename(columns={'Body': 'Answer_Body'})

merged_df = pd.merge(quesDataset, ansDataset, left_on='Id', right_on='ParentId')

#print("success")

# fuzzy search on question data set

from whoosh.fields import Schema, TEXT, ID
from whoosh import index, qparser
from whoosh.analysis import RegexTokenizer, LowercaseFilter
from whoosh.writing import BufferedWriter
from whoosh.qparser import FuzzyTermPlugin
import os

my_analyzer = RegexTokenizer() | LowercaseFilter()

# Define the schema for the index
schema = Schema(Body=TEXT(stored=True, analyzer=my_analyzer),Answer_Body=TEXT(stored=True, analyzer=my_analyzer))

# Create the index directory if it doesn't exist
if not os.path.exists("index_dir"):
    os.mkdir("index_dir")

# Create the index and add documents to it
ix = index.create_in("index_dir", schema)
writer= ix.writer()

for i, row in merged_df.iterrows():
    Body = remove_html_tags (row ["Body"])
    Answer_Body = remove_html_tags(row["Answer_Body"])
    writer.add_document(Body=Body,Answer_Body=Answer_Body)
    if i == 10000:
        break
writer.commit()



# Function to search the index
def index_search(dirname, search_fields, search_query):
    ix = index.open_dir(dirname)
    schema = ix.schema
    
    og = qparser.OrGroup.factory(0.8)
    mp = qparser.MultifieldParser(search_fields, schema, group=og)
    mp.add_plugin(FuzzyTermPlugin())
    q = mp.parse(search_query + "~")
    
    with ix.searcher() as searcher:
        results = searcher.search(q, limit=None)
        
        # Build a list of search results
        results_list = []
        for hit in results:
            result_dict = {}
            result_dict["QuestionBody"] = hit.fields()["Body"]
            result_dict["AnswerBody"] = hit.fields()["Answer_Body"]
            results_list.append(result_dict)
            
        return results_list


#Prompt the user for search queries
# while True:
#     query = input("Enter your query (or 0 to exit): ")
#     if query == "0":
#         break
#     else:
#         results = index_search("index_dir", ["Body"], query)
#         print("Search results:")
#         for i, result in enumerate(results, start=1):
#             print(f"{i}. Question: {result['QuestionBody']}")
#             print(f"   Answer: {result['AnswerBody']}")
#             print("")
# ------------------------------------------------------------------------------------------
# 
#                            FIND OVERLAPPING WORDS & DETECT TAGS                               
# 
# ------------------------------------------------------------------------------------------

# returns a DataFrame with the N most common words per tag
def getNCommonWords(DataFrame:pd.DataFrame, Column:str, n:int):
    grouped = DataFrame.groupby('Tag')
    return grouped[Column].apply(lambda x: pd.Series(str(x).split()).value_counts().head(n))

# returns a DataFrame with same data as getNCommonWords, but in a format easier to access
# better to use for graphing / accessing
def betterGetNCommonWords(DataFrame:pd.DataFrame, Column:str, n:int):
    df = getNCommonWords(DataFrame, Column, n)
    print(df)
    indice = df.values
    list = df.index.tolist()
    indices = []
    for i in indice:
        indices.append(i)
    wordFreq = {}
    wordFreqList = []
    for i in range(len(indices)):
        if(i != 0 and i%n == 0):
            wordFreqList.append(wordFreq)
            wordFreq = {}
        wordFreq[list[i][1]] = indices[i]
    wordFreqList.append(wordFreq)
    words = []
    for i in range(0, len(list), n):
        words.append(list[i][0])
    dff = pd.DataFrame()
    dff['Tags'] = words
    dff["'Word : Occurrences' list"] = wordFreqList
    print(dff)
    return dff

def commonWordsPerTag():
    grouper = qDataset.merge(tagDataset, left_on="Id", right_on="Id", how="inner")
    return betterGetNCommonWords(grouper, 'Title', 10) #set to 10 by default, use function separately to change number of words


# tag_common, all_common_words = commonWords(groups)
# overlap_words = overlappedCommonWords(tag_common, all_common_words)
# detectTags(qDataset, overlap_words)

# ------------------------------------------------------------------------------------------
# 
#                            CREATE DASH APP WITH GRAPHS/TABLES                               
# 
# ------------------------------------------------------------------------------------------

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

tagsDF = questionsPerTag(tagDataset)
QsPerMonthYear = questionsPerMonthAndYear(tagDataset, aDataset)
QsPerDay = questionsPerDay(qDataset)
sortedTopScoreOwners = topOwnerIdTag(tagDataset, aDataset)

fig = px.bar(tagsDF.head(20), x='Tag', y='Occurrences', barmode="group")                 # barchart showing most searched tags
fig2 = px.scatter(QsPerMonthYear, x='Date', y='Count')                                   # scatter graph showing year-month and no. of questions
fig3 = px.bar(QsPerDay, x='Date', y='QsAsked', barmode="group")                          # barchart showing date and no. of questions
app = dash.Dash()

filters = html.Div(children=[
    html.H1(children='Graph showing the top 20 most searched tags',style={'textAlign': 'center','font-family':'Arial'}),
    dcc.Graph(
        id='tag-graph',
        figure=fig
    ),
    html.H1(children='Table showing tags and frequency',style={'textAlign': 'center','font-family':'Arial'}),
    html.Div(dash_table.DataTable(
        tagsDF.to_dict('records'),
        columns=[
            {'name': 'Tag', 'id': 'Tag'},
            {'name': 'Frequency', 'id': 'Occurrences'},
        ],
        filter_action='native',
        page_size=20,
        fixed_rows={'headers': True},
        style_header={
            'backgroundColor': 'rgb(30, 30, 30)',
            'color': 'white',
        },
        style_data={
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
    )),
    html.H1(children='Graph showing questions asked by month and year',style={'textAlign': 'center','font-family':'Arial'}),
    dcc.Graph(
        id='MY-graph',
        figure=fig2
    ),
    html.H1(children='Graph showing the number of questions per day',style={'textAlign': 'center','font-family':'Arial'}),
    dcc.Graph(
        id='questions-graph',
        figure=fig3
    ),
    html.H1(children='Table showing top ID for each tag',
            style={
                'textAlign': 'center',
                'font-family' : 'Arial'
            }),
    html.Div(dash_table.DataTable(
        sortedTopScoreOwners.to_dict('records'),
        columns=[
            {'name': 'Issue', 'id': 'Tag'},
            {'name': 'ID no. of staff member', 'id': 'OwnerUserId'},
            {'name': 'Score', 'id': 'Score'},
        ],
        filter_action='native',
        page_size=20,
        fixed_rows={'headers': True},
        style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white',
            },
        style_data={
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
        ))
])

app.layout = html.Div(children=[filters])

if __name__ == '__main__':
    app.run_server(debug=True)