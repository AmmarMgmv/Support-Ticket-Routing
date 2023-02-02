# Tech Support Ticket Analytics

- create knowledge base on a person / team based on previous issues
- suggest / recomment the best person / team when a new request / incident happens

## Kaggle Dataset
https://www.kaggle.com/datasets/stackoverflow/stacksample


## Installation
```
> pip install pipenv
> pipenv install
```

## Technologies

1. Spacy - natural language processing
2. Whoosh - full text search
3. Pandas - data management
4. Dash - visualization

## Pseudo - code

1. Load csv data to pandas data frame
2. Preprocessing , remove stop words
3. Tokenize
4. Get top words
5. Create labels from top words
6. Tag ticket with multiple labels
7. Find the pattern from combination of labels occurring together
8. create knowledge base for each person based on issue answered and tags
9. Analytics : Get top words over time (per day) for trending
9. Admin Page: If no label : it is a new / emerging issue
10. If assigned a label check if its within a day-limit or week-limit from baseline (1.5*mean), then raise flag

## Code Snippet

### package dependency management
> Pipfile

```
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
dash = "*"
spacy = "*"
whoosh = "*"
pandas = "*"

[dev-packages]

[requires]
python_version = "3.9"

```
> main.py
```
import pandas
from spacy.lang.en import English

# loading dataset
questions_dataframe = pandas.read_csv('dataset/QuestionsHead.csv')

nlp = English()

# function to remove stopwords and html tags (non alpha words)
def remove_stopwords(text):
    if text:
        doc = nlp(text.lower())
        result = [token.text for token in doc if (token.text not in nlp.Defaults.stop_words) and (token.is_alpha or " " in token.lemma_)]
        return " ".join(result)
    else:
        return text

questions_dataframe["processed_title"] = questions_dataframe["Title"].fillna('').apply(remove_stopwords)

print(questions_dataframe[["Title", "processed_title"]].head())
```