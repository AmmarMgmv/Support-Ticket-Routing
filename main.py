import pandas as pd
from dataReader import askQuestions
import spacy
from lxml.html import fromstring
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer

#still contains: 'lemmatizer', 'tagger
nlp = spacy.load("en_core_web_sm", exclude=['parser','tok2vec','attribute_ruler', 'ner']) 
print(nlp.pipe_names)


# Import the datasets (changed encoding as default is utf-8, which
# does not support some characters in the datasets
tagDataset = pd.read_csv("Dataset\Tags.csv", encoding = "ISO-8859-1")
qDataset = pd.read_csv("Dataset\Questions.csv", encoding = "ISO-8859-1")
aDataset = pd.read_csv("Dataset\Answers.csv", encoding = "ISO-8859-1")


#askQuestions(tagDataset, qDataset, aDataset)

#   remove html tags in the body of questions
def remove_tags(text):
    toParse = fromstring(text)
    #return str(toParse.text_content())
    return str(toParse.text_content()).replace('\n', '')

# remove stopwords from a column `column` in a DataFrame `dataframe`
# returns a list to be used by replacing worked on column or adding as a new column
def remove_stopwords(dataframe: pd.DataFrame , column: str) -> list:
    cleanedColumn = []
    for text in nlp.pipe(dataframe[column], disable=['lemmatizer', 'tagger']):
        cleanedText = [token.text for token in text if not token.is_stop and not token.is_punct]
        cleanedColumn.append(" ".join(cleanedText))
    return cleanedColumn

# lemmatize all words from a column `column` in a DataFrame `dataframe`
# returns a list to be used by replacing worked on column or adding as a new column
def lemmatize(dataframe: pd.DataFrame, column: str) -> list:
    lematizedColumn = []
    for text in nlp.pipe(dataframe[column], disable=['tagger']):
        lemmatizedText = [token.lemma_ for token in text]
        lematizedColumn.append(" ".join(lemmatizedText))
    return lematizedColumn

# remove all stop words and lemmatize all words from a column `column` in a DataFrame `dataframe`
# returns a list to be used by replacing worked on column or adding as a new column
def cleanAndLemmatize(dataframe: pd.DataFrame, column: str) -> list:
    lematizedColumn = []
    for text in nlp.pipe(dataframe[column], disable=['tagger']):
        lemmatizedText = [token.lemma_ for token in text if not token.is_stop and not token.is_punct]
        lematizedColumn.append(" ".join(lemmatizedText))
    return lematizedColumn

# remove all stop words and POS tag all words from a column `column` in a DataFrame `dataframe`
# returns a list to be used by replacing worked on column or adding as a new column
def posTag(dataframe: pd.DataFrame, column: str) -> list:
    posTagged = []
    for text in nlp.pipe(dataframe[column]):
        posTags = [(token.text, token.pos_) for token in text if not token.is_stop and not token.is_punct]
        posTagged.append(posTags)
    return posTagged

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

# Get most common/top words for each tag
for name, group in groups:
    # Join Title and Body columns
    text = group['Title'].str.cat(group['Body'], sep=' ')
    # Replace NaN values with an empty string
    text = text.fillna('')
    # Count how many times a word appears
    count_vectorizer = CountVectorizer()
    word_counts = count_vectorizer.fit_transform(text)
    # Find what the most common words are
    word_count_dict = dict(zip(count_vectorizer.get_feature_names_out(), word_counts.sum(axis=0).tolist()[0]))
    most_common_words = Counter(word_count_dict).most_common(5)
    print(f"Most common words for tag '{name}':")
    print(most_common_words)

#print(TagsQs.head())

#   post-tagging: get nouns, verbs etc.
#   get the text of Qdatabase titile and body
# QTitle = nlp(qDataset['Title'])
# QBody = nlp(qDataset['Body'])
# for text in QTitle:
#     print(text.text, text.pos_)     # post-tagging for the title
# for text in QBody:
#     print(text.text, text.pos_)     # post-tagging for the body

