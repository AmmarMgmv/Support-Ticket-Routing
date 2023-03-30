import dash
import pandas as pd
import re
import os
import dash_bootstrap_components as dbc
from whoosh import index, qparser
from whoosh.fields import Schema, TEXT
from whoosh.qparser import FuzzyTermPlugin
from whoosh.analysis import RegexTokenizer, LowercaseFilter
from apps import dataManipulator, dataReader

# ------------------------------------------------------------------------------------------
# 
#                               LOAD IN THE DATASETS                               
# 
# ------------------------------------------------------------------------------------------

# Import the datasets (changed encoding as default is utf-8, which
# does not support some characters in the datasets
# tagDataset = pd.read_csv("Dataset\Tags.csv", encoding = "ISO-8859-1")
# qDataset = pd.read_csv("Dataset\Questions.csv", encoding = "ISO-8859-1")
# aDataset = pd.read_csv("Dataset\Answers.csv", encoding = "ISO-8859-1")

# ## FOR DEBUG: temporarily reads the first 200 rows of csv files
tagDataset = pd.read_csv("Dataset\Tags.csv", encoding = "ISO-8859-1")
qDataset = pd.read_csv("Dataset\Questions.csv", nrows = 1000, encoding = "ISO-8859-1")
aDataset = pd.read_csv("Dataset\Answers.csv", nrows = 1000, encoding = "ISO-8859-1")

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

TagsQs = pd.merge(tagDataset, qDataset[["Id", "Title", "Body"]], on="Id")
groups = TagsQs.groupby('Tag')

# ------------------------------------------------------------------------------------------
# 
#                                  FUZZY SEARCH ALGORITHM                               
# 
# ------------------------------------------------------------------------------------------

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

columns_to_read_ids = ['Ids', 'FirstName', 'LastName']
engineerDataset= pd.read_csv("Dataset\EngineersDataset.csv",encoding = "ISO-8859-1", usecols=columns_to_read_ids)

merged_df = pd.merge(quesDataset, ansDataset, left_on='Id', right_on='ParentId')
final_df = pd.merge(merged_df, engineerDataset, left_on='Id', right_on='Ids')

# fuzzy search on question data set
my_analyzer = RegexTokenizer() | LowercaseFilter()

# Define the schema for the index
schema = Schema(Body=TEXT(stored=True, analyzer=my_analyzer),Answer_Body=TEXT(stored=True, analyzer=my_analyzer),Ids=TEXT(stored=True, analyzer=my_analyzer),FirstName=TEXT(stored=True, analyzer=my_analyzer),LastName=TEXT(stored=True, analyzer=my_analyzer))

# Create the index directory if it doesn't exist
if not os.path.exists("index_dir"):
    os.mkdir("index_dir")

# Create the index and add documents to it
ix = index.create_in("index_dir", schema)
writer= ix.writer()

for i, row in final_df.iterrows():
    Body = remove_html_tags (row ["Body"])
    Answer_Body = remove_html_tags(row["Answer_Body"])
    Ids = str(row['Ids'])
    FirstName = row['FirstName']
    LastName = row['LastName']
    writer.add_document(Body=Body,Answer_Body=Answer_Body,Ids=Ids,FirstName=FirstName,LastName=LastName)
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
            result_dict["Ids"] = hit.fields()["Ids"]
            result_dict["FirstName"] = hit.fields()["FirstName"]
            result_dict["LastName"] = hit.fields()["LastName"]
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
#             print(f"     Answer: {result['AnswerBody']}")
#             print(f"     Id: {result['Ids']}")
#             print(f"     Name: {result['FirstName']} {result['LastName']}")
#             print("")

# ------------------------------------------------------------------------------------------
# 
#                            FIND OVERLAPPING WORDS & DETECT TAGS                               
# 
# ------------------------------------------------------------------------------------------

# returns a DataFrame with the N most common words per tag
# def getNCommonWords(DataFrame:pd.DataFrame, Column:str, n:int):
#     grouped = DataFrame.groupby('Tag')
#     return grouped[Column].apply(lambda x: pd.Series(str(x).split()).value_counts().head(n))

# returns a DataFrame with same data as getNCommonWords, but in a format easier to access
# better to use for graphing / accessing
# def betterGetNCommonWords(DataFrame:pd.DataFrame, Column:str, n:int):
#     df = getNCommonWords(DataFrame, Column, n)
#     print(df)
#     indice = df.values
#     list = df.index.tolist()
#     indices = []
#     for i in indice:
#         indices.append(i)
#     wordFreq = {}
#     wordFreqList = []
#     for i in range(len(indices)):
#         if(i != 0 and i%n == 0):
#             wordFreqList.append(wordFreq)
#             wordFreq = {}
#         wordFreq[list[i][1]] = indices[i]
#     wordFreqList.append(wordFreq)
#     words = []
#     for i in range(0, len(list), n):
#         words.append(list[i][0])
#     dff = pd.DataFrame()
#     dff['Tags'] = words
#     dff["'Word : Occurrences' list"] = wordFreqList
#     print(dff)
#     return dff

# def commonWordsPerTag():
#     grouper = qDataset.merge(tagDataset, left_on="Id", right_on="Id", how="inner")
#     return betterGetNCommonWords(grouper, 'Title', 10) #set to 10 by default, use function separately to change number of words


tag_common, all_common_words = dataManipulator.commonWords(groups)
overlap_words = dataManipulator.overlappedCommonWords(tag_common, all_common_words)
# detectTags(qDataset, overlap_words)

# ------------------------------------------------------------------------------------------
# 
#                            CREATE DASH APP WITH GRAPHS/TABLES                               
# 
# ------------------------------------------------------------------------------------------

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR])
server = app.server