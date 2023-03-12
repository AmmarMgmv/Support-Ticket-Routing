# import the package to work on the datasets
import pandas as pd
import spacy
from lxml.html import fromstring
import re

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

#load the datasets 
qDataset = pd.read_csv("Dataset\Questions.csv", encoding = "ISO-8859-1")

# fuzzy search on question data set

from whoosh.fields import Schema, TEXT, ID
from whoosh import index, qparser
from whoosh.analysis import RegexTokenizer, LowercaseFilter
from whoosh.writing import BufferedWriter
from whoosh.qparser import FuzzyTermPlugin
import os

my_analyzer = RegexTokenizer() | LowercaseFilter()

# Define the schema for the index
schema = Schema(Body=TEXT(stored=True, analyzer=my_analyzer))

# Create the index directory if it doesn't exist
if not os.path.exists("index_dir"):
    os.mkdir("index_dir")

# Create the index and add documents to it
ix = index.create_in("index_dir", schema)
writer= ix.writer()

for i, row in qDataset.iterrows():
    Body = remove_html_tags (row ["Body"])
    ##answerBody = remove_html_tags(row["answerBody"])
    writer.add_document(Body=Body)
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
        results = searcher.search(q, limit=5)
        
        # Build a dictionary of search results
        results_dict = {}
        for hit in results:
            results_dict[hit.fields()["Body"]] = hit.score
            
        return results_dict


#Prompt the user for search queries
while True:
    query = input("Enter your query (or 0 to exit): ")
    if query == "0":
        break
    else:
        results = index_search("index_dir", ["Body"], query)
        print("Search results:")
        for i, result in enumerate(results, start=1):
         print(f"{i}. {result}\n")