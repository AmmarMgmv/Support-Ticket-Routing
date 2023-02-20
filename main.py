
from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output
import pandas as pd

tagDataset = pd.read_csv("Dataset\Tags.csv", encoding = "ISO-8859-1")
qDataset = pd.read_csv("Dataset\Questions.csv", encoding = "ISO-8859-1")
aDataset = pd.read_csv("Dataset\Answers.csv", encoding = "ISO-8859-1")

TagsAnswers = pd.merge(tagDataset, aDataset, left_on='Id', right_on='ParentId')
summedScore = TagsAnswers.groupby(['Tag', 'OwnerUserId'])['Score'].sum().reset_index()
topScoreOwners = summedScore.groupby('Tag').agg({'Score': 'idxmax'}).reset_index()
topScoreOwners = summedScore.iloc[topScoreOwners['Score']]
sortedTopScoreOwners = topScoreOwners.sort_values('Score', ascending=False)
df=sortedTopScoreOwners

#table that shows top userID by tag and their score, also allows to user to search
#------------------------------------------------------------------------------
app = Dash(__name__)

app.layout = dash_table.DataTable(
    df.to_dict('records'),
     columns=[
        {'name': 'Issue', 'id': 'Tag'},
        {'name': 'ID no. of staff member', 'id': 'OwnerUserId'},
        {'name': 'Score', 'id': 'Score'},
    ],
    filter_action='native',

    style_table={
        'height': 15,
    },
    style_data={
        'width': '180 px', 'minWidth': '180 px', 'maxWidth': '180 px',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
    },
    )

if __name__ == '__main__':
    app.run_server(debug=True)
