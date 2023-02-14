import pandas as pd
import plotly.express as px

tagDataset = pd.read_csv("Dataset\Tags.csv", encoding = "ISO-8859-1")
qDataset = pd.read_csv("Dataset\Questions.csv", encoding = "ISO-8859-1")


#pie chart to show the top queried tags

sortedTags = tagDataset.groupby(["Tag"]).size() 
sortByTop = sortedTags.sort_values(ascending=False)
data = pd.DataFrame({'Tag': sortByTop.index, 'Occurrences': sortByTop.values})

#Using the top 15 queried tags to display
data = data.head(15)
fig = px.pie(data, values='Occurrences', names='Tag', title='No. of questions by tag')
fig.show()


#bar chart to show the number of queries by year

datesByYear = pd.DataFrame(pd.to_datetime(qDataset["CreationDate"]).dt.year)
sortedDates = datesByYear.groupby(["CreationDate"]).size()
fig = px.bar(sortedDates, x=sortedDates.index, y=0, title='Number of queries by year', labels={0:'No. of Queries'})
fig.show()
