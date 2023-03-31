import pandas as pd

# This function calls on all the functions below
# def askQuestions(tData, qData, aData):
#     uniqueTags(tData)
#     uniqueOwnerId(qData, aData)
#     questionsPerTag(tData)
#     questionsPerOwner(qData, aData)
#     questionsPerDay(qData)
#     questionsPerTagPerDay(tData, qData)
#     topOwnerIdTag(tData, aData)
#     answersPerQuestion(aData)
#     unansweredQuestions(qData, aData)
#     questionsPerMonthAndYear(tData, qData)

# This function gets the list and count of unique first names
def findUniqueFirstNames(datasetE):
    #loc: choose column by name
    firstNames = datasetE.loc[:,"FirstName"] 
    uniqueFirstNames = pd.unique(firstNames) 
    return uniqueFirstNames

# This function gets the list and count of unique last names
def findUniqueLastNames(datasetE):
    #loc: choose column by name
    lastNames = datasetE.loc[:,"LastName"] 
    uniqueLastNames = pd.unique(lastNames) 
    return uniqueLastNames

# This function gets the list and count of unique tags
def uniqueTags(datasetT):
    #loc: choose column by name
    tags = datasetT.loc[:,"Tag"] 
    uniqueTags = pd.unique(tags) 
    return uniqueTags


# This function gets the list and count of unique owner ID's
def uniqueOwnerId(DatasetQ, DatasetA):
    qOwner = DatasetQ.loc[:, "OwnerUserId"]
    aOwner = DatasetA.loc[:, "OwnerUserId"]
    owners = pd.concat([qOwner, aOwner])
    uniqueOwners = pd.unique(owners)   
    # Gets rid of invalid values and converts ID to int type 
    filteredUniqueOwners = pd.Series(uniqueOwners).dropna().astype('int').values 


# This function counts the number of questions per tag and sorts in descending order
def questionsPerTag(datasetT):
    sortedTags = datasetT.groupby(["Tag"]).size() #count how many in each "group: "Tag" "
    sortByTop = sortedTags.sort_values(ascending=False) #sort to show top categories
    tagsDF = pd.DataFrame({'Tag': sortByTop.index, 'Occurrences': sortByTop.values})
    return tagsDF

# This function gets the number of questions asked by each owner and in each category
def questionsPerOwner(datasetQ, datasetA):
    sortedQs = datasetQ.groupby(["OwnerUserId"]).size()
    sortedAns = datasetA.groupby(["ParentId"]).size()

# This function counts the number of questions per day
def questionsPerDay(datasetQ):
    format = "%Y-%m-%d"
    dates = pd.DataFrame(pd.to_datetime(datasetQ["CreationDate"]).dt.strftime(format))
    sortedDates = dates.groupby(["CreationDate"]).size()
    qsPerDay = pd.DataFrame({"Date": sortedDates.index, "QsAsked": sortedDates.values})
    return qsPerDay


# This function counts the number of questions per tag per day
def questionsPerTagPerDay(datasetT, datasetQ):
    # Merge the "Tags" and "Questions" datasets on the "Id" column
    TagsQuestions = pd.merge(datasetT, datasetQ, on="Id", how="inner")
    # Convert the "CreationDate" column to a datetime type and make it a new column
    TagsQuestions['CreationDate'] = pd.to_datetime(TagsQuestions['CreationDate'])
    TagsQuestions['Day'] = TagsQuestions['CreationDate'].dt.date
    # Group by "Day" and "Tag" columns, then count number of occurrences for each group
    QsPerTagPerDay = TagsQuestions.groupby(["Day", "Tag"]).size().reset_index(name="Count")
    # Fill any missing values with 0
    QsPerTagPerDay = QsPerTagPerDay.fillna(0)
    return QsPerTagPerDay


# This function gets the top ownerId answering in each tag
def topOwnerIdTag(datasetT, datasetA):
    # Merge "Tags" and "Answers" datasets on their respective corresponding "Id" column
    TagsAnswers = pd.merge(datasetT, datasetA, left_on='Id', right_on='ParentId')
    # Group the merged DataFrame by Tag and OwnerUserId and calculate the sum of the Score for each group
    summedScore = TagsAnswers.groupby(['Tag', 'OwnerUserId'])['Score'].sum().reset_index()
    # Get the OwnerUserId with the highest Score for each Tag
    topScoreOwners = summedScore.groupby('Tag').agg({'Score': 'idxmax'}).reset_index()
    topScoreOwners = summedScore.iloc[topScoreOwners['Score']]
    # Sort by score to view top
    sortedTopScoreOwners = topScoreOwners.sort_values('Score', ascending=False)
    return sortedTopScoreOwners


# This function gets the number of answers per question
def answersPerQuestion(datasetA):
    NumOfAns = datasetA.groupby(['ParentId']).size() #count ParentID in aDataset to see how many answers for each question


# This function gets the unanswered questions
def unansweredQuestions(datasetQ, datasetA):
    unanswered = datasetQ[~datasetQ["Id"].isin(datasetA["ParentId"])]
    
# This function gets the number of questions per month of each year
def questionsPerMonthAndYear(datasetT, datasetQ):
    TagsQuestions = pd.merge(datasetT, datasetQ, on="Id", how="inner")
    TagsQuestions['CreationDate'] = pd.to_datetime(TagsQuestions['CreationDate'])
    format = "%Y-%m"
    dates = pd.DataFrame(pd.to_datetime(datasetQ["CreationDate"]).dt.strftime(format))
    sortedDates = dates.groupby(["CreationDate"]).size()
    QsPerMonthYear = pd.DataFrame({'Date' : sortedDates.index, 'Count' : sortedDates.values})
    return QsPerMonthYear
