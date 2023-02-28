import pandas as pd

# This function calls on all the functions below
def askQuestions(tData, qData, aData):
    uniqueTags(tData)
    uniqueOwnerId(qData, aData)
    questionsPerTag(tData)
    questionsPerOwner(qData, aData)
    questionsPerDay(qData)
    questionsPerTagPerDay(tData, qData)
    topOwnerIdTag(tData, aData)
    answersPerQuestion(aData)
    unansweredQuestions(qData, aData)
    questionsPerMonthAndYear(tData, qData)

# This function gets the list and count of unique tags
def uniqueTags(datasetT):
    #loc: choose column by name
    tags = datasetT.loc[:,"Tag"] 
    uniqueTags = pd.unique(tags) 
    print("Question 1: Get the list and count of unique tags")
    print(uniqueTags, "\nNumber of tags: ", len(uniqueTags), "\n")


# This function gets the list and count of unique owner ID's
def uniqueOwnerId(DatasetQ, DatasetA):
    qOwner = DatasetQ.loc[:, "OwnerUserId"]
    aOwner = DatasetA.loc[:, "OwnerUserId"]
    owners = pd.concat([qOwner, aOwner])
    uniqueOwners = pd.unique(owners)   
    # Gets rid of invalid values and converts ID to int type 
    filteredUniqueOwners = pd.Series(uniqueOwners).dropna().astype('int').values 
    print("Question 2: Get the list and count of unique owner ID's")
    print("Unique ID's in floating point representation: ", uniqueOwners, "\nNumber of owner id's: ", len(uniqueOwners))
    print("Unique ID's in integer representation: ", filteredUniqueOwners, "\nNumber of owner id's: ", len(filteredUniqueOwners), "\n")


# This function counts the number of questions per tag and sorts in descending order
def questionsPerTag(datasetT):
    sortedTags = datasetT.groupby(["Tag"]).size() #count how many in each "group: "Tag" "
    sortByTop = sortedTags.sort_values(ascending=False) #sort to show top categories
    tagsDF = pd.DataFrame({'Tag': sortByTop.index, 'Occurrences': sortByTop.values})
    print("Question 3: Count the number of questions per tag and sorts in descending order")
    print("Tags sorted from most used to least used: \n", sortByTop, "\nTop tag: ", sortByTop.index[0], "\n")
    return tagsDF

# This function gets the number of questions asked by each owner and in each category
def questionsPerOwner(datasetQ, datasetA):
    print("Question 4: Get the number of questions asked by each owner and in each category\n")
    sortedQs = datasetQ.groupby(["OwnerUserId"]).size()
    print("Question 4: Questions Dataset:\n", sortedQs, "\n")
    sortedAns = datasetA.groupby(["ParentId"]).size()
    print("Question 4: Answers Dataset:\n", sortedAns, "\n")
    print()


# This function counts the number of questions per day
def questionsPerDay(datasetQ):
    format = "%Y-%m-%d"
    dates = pd.DataFrame(pd.to_datetime(datasetQ["CreationDate"]).dt.strftime(format))
    sortedDates = dates.groupby(["CreationDate"]).size()
    qsPerDay = pd.DataFrame({"Date": sortedDates.index, "QsAsked": sortedDates.values})
    print("Question 5: Count the number of questions per day\n", sortedDates, "\n")
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
    print("Question 6: Count the number of questions per tag per day\n", QsPerTagPerDay, "\n")
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
    print("Question 7: Get the top ownerId answering in each tag\n", sortedTopScoreOwners, "\n")
    return sortedTopScoreOwners


# This function gets the number of answers per question
def answersPerQuestion(datasetA):
    NumOfAns = datasetA.groupby(['ParentId']).size() #count ParentID in aDataset to see how many answers for each question
    print("Question 8: Get the number of answers per question\n", NumOfAns, "\n")


# This function gets the unanswered questions
def unansweredQuestions(datasetQ, datasetA):
    unanswered = datasetQ[~datasetQ["Id"].isin(datasetA["ParentId"])]
    print("Question 9: Find the questions which are still not answered\n", unanswered['Title'])
    
# This function gets the number of questions per month of each year
def questionsPerMonthAndYear(datasetT, datasetQ):
    TagsQuestions = pd.merge(datasetT, datasetQ, on="Id", how="inner")
    TagsQuestions['CreationDate'] = pd.to_datetime(TagsQuestions['CreationDate'])
    format = "%Y-%m"
    dates = pd.DataFrame(pd.to_datetime(datasetQ["CreationDate"]).dt.strftime(format))
    sortedDates = dates.groupby(["CreationDate"]).size()
    QsPerMonthYear = pd.DataFrame({'Date' : sortedDates.index, 'Count' : sortedDates.values})
    return QsPerMonthYear
