# import the package to work on the datasets
import pandas as pd
import spacy
from lxml.html import fromstring

#still contains: 'lemmatizer', 'tagger
##nlp = spacy.load("en_core_web_sm", exclude=['parser','tok2vec','attribute_ruler', 'ner']) 
##print(nlp.pipe_names)

# import the datasets to be worked with (changed encoding as default is utf-8, which
# does not support some characters in the datasets
#tagDataset = pd.read_csv("Dataset\Tags.csv", encoding = "ISO-8859-1")
qDataset = pd.read_csv("Dataset\Questions_cleaned.csv", encoding = "ISO-8859-1")
#aDataset = pd.read_csv("Dataset\Answers.csv", encoding = "ISO-8859-1")

#1.       get the list of Unique tags. (+count the unique tags)
# tags = tagDataset.loc[:,"Tag"] #loc: choose column by name

# uniqueTags = pd.unique(tags) #get unique tags
# ##print("Question 1: Get the list of Unique tags. (+count the unique tags)")
# ##print(uniqueTags, "\nNumber of tags: ", len(uniqueTags), "\n")

# # 2.       get the list and count of unique ownerIds
# qOwner = qDataset.loc[:, "OwnerUserId"]
# aOwner = aDataset.loc[:, "OwnerUserId"]

# owners = pd.concat([qOwner, aOwner]) #combine the 2 above lists
# uniqueOwners = pd.unique(owners)
# filteredUniqueOwners = pd.Series(uniqueOwners).dropna().astype('int').values #gets rid of invalid values and converts ID to int type
# ##print("Question 2: Get the list and count of unique ownerIds")
# ##print("Unique ID's in floating point representation: ", uniqueOwners, "\nNumber of owner id's: ", len(uniqueOwners))
# ##print("Unique ID's in integer representation: ", filteredUniqueOwners, "\nNumber of owner id's: ", len(filteredUniqueOwners), "\n")

# # 3.       Count number of question per tag ( + get top category )
# sortedTags = tagDataset.groupby(["Tag"]).size() #count how many in each "group: "Tag" "
# sortByTop = sortedTags.sort_values(ascending=False) #sort to show top categories
# ##print("Question 3: Count number of question per tag ( + get top category )")
# ##print("Tags sorted from most used to least used: \n", sortByTop, "\n")

# # 4.       get number of question asked by each owner / and in each category (same for answers dataset)
# sortedQs = qDataset.groupby(["OwnerUserId"]).size()
# ##print("Question 4: Get number of question asked by each owner / and in each category\n")
# ##print(sortedQs, "\n")
# #  answers datasheet
# sortedAns = aDataset.groupby(["ParentId"]).size()
# ##print("Question 4: Get number of questions answered by each owner / and in each category\n")
# ##print(sortedAns, "\n")

# # 5.       count Number of questions per day
# format = "%Y-%m-%d"
# dates = pd.DataFrame(pd.to_datetime(qDataset["CreationDate"]).dt.strftime(format))
# sortedDates = dates.groupby(["CreationDate"]).size()
# ##print("Question 5: Count Number of questions per day\n")
# ##print(sortedDates, "\n")

# # 6.       Count number of questions in each tags per day
# # Merge the "Tags" and "Questions" datasets on the "Id" column
# TagsQuestions = pd.merge(tagDataset, qDataset, on="Id", how="inner")
# # Convert the "CreationDate" column to a datetime type and make it a new column
# TagsQuestions['CreationDate'] = pd.to_datetime(TagsQuestions['CreationDate'])
# TagsQuestions['Day'] = TagsQuestions['CreationDate'].dt.date
# # Group by "Day" and "Tag" columns, then count number of occurrences for each group
# grouped = TagsQuestions.groupby(["Day", "Tag"]).size().reset_index(name="Count")
# # Pivot the DataFrame so that the "Tag" column becomes a row index and the "Day" column becomes a column
# QsPerTagPerDay = grouped.pivot(index="Tag", columns="Day", values="Count")
# # Fill any missing values with 0
# QsPerTagPerDay = QsPerTagPerDay.fillna(0)
# ##print("Question 6: Count number of questions in each tags per day\n")
# ##print(QsPerTagPerDay, "\n")


# # 7.       get the top ownerId answering in each tags
# # Merge "Tags" and "Answers" datasets on their respective corresponding "Id" column
# TagsAnswers = pd.merge(tagDataset, aDataset, left_on='Id', right_on='ParentId')
# # Group the merged DataFrame by Tag and OwnerUserId and calculate the sum of the Score for each group
# summedScore = TagsAnswers.groupby(['Tag', 'OwnerUserId'])['Score'].sum().reset_index()
# # Get the OwnerUserId with the highest Score for each Tag
# topScoreOwners = summedScore.groupby('Tag').agg({'Score': 'idxmax'}).reset_index()
# topScoreOwners = summedScore.iloc[topScoreOwners['Score']]
# #sort by score to view top
# sortedTopScoreOwners = topScoreOwners.sort_values('Score', ascending=False)
# ##print("Question 7: get the top ownerId answering in each tags\n")
# ##print(sortedTopScoreOwners, "\n")


# # 8.       number of answers per question
# NumOfAns = aDataset.groupby(['ParentId']).size() #count ParentID in aDataset to see how many answers for each question
# ##print("Question 8: number of answers per question\n")
# ##print(NumOfAns, "\n")


# #9.       Find the questions which are still not answered?
# unanswered = qDataset[~qDataset["Id"].isin(aDataset["ParentId"])]
# ##print("Question 9: Find the questions which are still not answered\n")
# ##print(unanswered)

# print("successful")

# #   remove html tags in the body of questions
# def remove_tags(text):
#     toParse = fromstring(text)
#     return str(toParse.text_content())



# # remove stopwords from a column `column` in a DataFrame `dataframe`
# # returns a list to be used by replacing worked on column or adding as a new column
# def remove_stopwords(dataframe: pd.DataFrame , column: str) -> list:
#     cleanedColumn = []
#     for text in nlp.pipe(dataframe[column], disable=['lemmatizer', 'tagger']):
#         cleanedText = [token.text for token in text if not token.is_stop and not token.is_punct]
#         cleanedColumn.append(" ".join(cleanedText))
#     return cleanedColumn

# # lemmatize all words from a column `column` in a DataFrame `dataframe`
# # returns a list to be used by replacing worked on column or adding as a new column
# def lemmatize(dataframe: pd.DataFrame, column: str) -> list:
#     lematizedColumn = []
#     for text in nlp.pipe(dataframe[column], disable=['tagger']):
#         lemmatizedText = [token.lemma_ for token in text]
#         lematizedColumn.append(" ".join(lemmatizedText))
#     return lematizedColumn


# # remove all stop words and lemmatize all words from a column `column` in a DataFrame `dataframe`
# # returns a list to be used by replacing worked on column or adding as a new column
# def cleanAndLemmatize(dataframe: pd.DataFrame, column: str) -> list:
#     lematizedColumn = []
#     for text in nlp.pipe(dataframe[column], disable=['tagger']):
#         lemmatizedText = [token.lemma_ for token in text if not token.is_stop and not token.is_punct]
#         lematizedColumn.append(" ".join(lemmatizedText))
#     return lematizedColumn


#   remove stop words and html tags for both title and body parts of each tag
# qDataset['Cleaned Body'] = qDataset['Body'].apply(remove_tags)
# qDataset['Cleaned Title'] = remove_stopwords(qDataset, 'Title')
# qDataset['Cleaned Body'] = remove_stopwords(qDataset, 'Cleaned Body')

# print(qDataset[["Title", "Cleaned Title"]].head(3))
# print(qDataset[["Body", "Cleaned Body"]].head(3))

# qDataset['Title'] = qDataset['Cleaned Title']
# qDataset['Body'] = qDataset['Cleaned Body']
# qDataset.drop('Cleaned Title', axis=1, inplace=True) #replace and remove 'Cleaned Title' column    # axis=1 means delete a column
# qDataset.drop('Cleaned Body', axis=1, inplace=True) #replace and remove 'Cleaned Body' column      # axis=0 would mean delete a row
# TagsQs = pd.merge(tagDataset, qDataset[["Id", "Title", "Body"]], on="Id")
# print("successful")

# fuzzy search on question data set

from whoosh.fields import Schema, TEXT
from whoosh import index, qparser
from whoosh.analysis import RegexTokenizer
from whoosh.writing import BufferedWriter
from whoosh.qparser import FuzzyTermPlugin
import os

# Define the schema for the index
schema = Schema(Body=TEXT(stored=True, analyzer=RegexTokenizer()))

# Create the index directory if it doesn't exist
if not os.path.exists("index_dir"):
    os.mkdir("index_dir")

# Create the index and add documents to it
ix = index.create_in("index_dir", schema)
writer= ix.writer()

for i, row in qDataset.iterrows():
    Body = row["Body"]
    writer.add_document(Body=Body)
    if i == 20:
        break
writer.commit()




# Function to search the index
def index_search(dirname, search_fields, search_query):
    ix = index.open_dir(dirname)
    schema = ix.schema
    
    og = qparser.OrGroup.factory(0.9)
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
        for result in results:
            print(result + "\n")