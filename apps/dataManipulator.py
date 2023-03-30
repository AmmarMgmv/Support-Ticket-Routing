import pandas as pd
import spacy
from typing import List
from apps import dataReader
from collections import Counter
from lxml.html import fromstring
from sklearn.feature_extraction.text import CountVectorizer

#still contains: 'lemmatizer', 'tagger', 'attribute_ruler'
nlp = spacy.load("en_core_web_sm", exclude=['parser','tok2vec', 'ner']) 
# print(nlp.pipe_names)

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
    for text in nlp.pipe(dataframe[column]):
        lemmatizedText = [token.lemma_ for token in text]
        lematizedColumn.append(" ".join(lemmatizedText))
    return lematizedColumn

# remove all stop words and lemmatize all words from a column `column` in a DataFrame `dataframe`
# returns a list to be used by replacing worked on column or adding as a new column
def cleanAndLemmatize(dataframe: pd.DataFrame, column: str) -> list:
    lematizedColumn = []
    for text in nlp.pipe(dataframe[column]):
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

# Get most common/top words for each tag
## put all the common words obtained above in a list
def commonWords(groups: pd.DataFrame) -> tuple[dict, list]:
    tag_common = {}
    all_common_words = []
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
        common = []
        for word in most_common_words:
            common.append(word[0])
        all_common_words += common
        tag_common.update({name: common})
        # print(f"Most common words for tag '{name}':")
        # print(most_common_words)
    return tag_common, all_common_words


# Get overlapped common words over tags
def overlappedCommonWords(tag_common : dict, all_common: List[str]) -> dict:
    # find overlapping words across tags
    overlap_words = {}
    # check for overlapping words and add them to overlap_words{}
    # print("Overlapping words accross tags: ")
    already_checked = []
    for key in tag_common:
        for num in range(5):
            count = 0
            for item in all_common:
                if tag_common[key][num] == item:
                    count = count + 1
            if count > 1 and tag_common[key][num] not in already_checked:
                already_checked.append(tag_common[key][num])
                # print(f"The word '{tag_common[key][num]}' overlaps {str(count)} times in the following tags: ")
                tag = []
                for key_overlap in tag_common:
                    if tag_common[key][num] in tag_common[key_overlap]:
                        tag.append(key_overlap)
                        # print(key_overlap)
                # add the overlapping words and corresponding tags to overlap_words{}
                overlap_words[tag_common[key][num]] = tag
    return overlap_words


# Detect tags for the question taken from user input
def detectTagsFromInput(overlap: dict, input) -> list:
    text = []
    # Split each question into a list of words
    words = input.split()
    # Join the tag names for each word in the question together in a string
    for word in words:
        try:
            text.append(' '.join(overlap[word]))
        except KeyError:
            pass
    # Count and find the 5 most common tags in the question
    try:
        count_vectorizer = CountVectorizer()
        tag_counts = count_vectorizer.fit_transform(text)
        tag_count_dict = dict(zip(count_vectorizer.get_feature_names_out(), tag_counts.sum(axis=0).tolist()[0]))
        most_common_tags = Counter(tag_count_dict).most_common(5)
        # print(f"Most common tags for question '{question}':")
        print(most_common_tags)
        common = []
        for word in most_common_tags:
            common.append(word[0])
    except ValueError:
        print("No tag detected for question {}")
        common = ['']
        pass
    return common

    # ## Create a new dataframe with common words connected to each tag
# TagsCommons = pd.DataFrame(tag_common.items(), columns=['Tag', 'Common Words'])


# # put all the common words obtained above in a list
# all_common_words = []
# all_common_words = []
# for key in TagsCommons:
#     for num in range(5):
#         all_common_words.append(tag_common[key][num])