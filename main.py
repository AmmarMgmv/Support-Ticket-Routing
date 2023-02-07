# import the package to work on the datasets
import pandas as pd

# import the datasets to be worked with (changed encoding as default is utf-8, which
# does not support some characters in the datasets
tagDataset = pd.read_csv("Dataset\Tags.csv", encoding = "ISO-8859-1")
qDataset = pd.read_csv("Dataset\Questions.csv", encoding = "ISO-8859-1")
aDataset = pd.read_csv("Dataset\Answers.csv", encoding = "ISO-8859-1")

#1.       get the list of Unique tags. (+count the unique tags)
tags = tagDataset.loc[:,"Tag"] #loc: choose column by name

uniqueTags = pd.unique(tags) #get unique tags
print("Question 1: Get the list of Unique tags. (+count the unique tags)")
print(uniqueTags, "\nNumber of tags: ", len(uniqueTags), "\n")

# 2.       get the list and count of unique ownerIds
qOwner = qDataset.loc[:, "OwnerUserId"]
aOwner = aDataset.loc[:, "OwnerUserId"]

owners = pd.concat([qOwner, aOwner]) #combine the 2 above lists
uniqueOwners = pd.unique(owners)    
filteredUniqueOwners = pd.Series(uniqueOwners).dropna().astype('int').values #gets rid of invalid values and converts ID to int type
print("Question 2: Get the list and count of unique ownerIds")
print("Unique ID's in floating point representation: ", uniqueOwners, "\nNumber of owner id's: ", len(uniqueOwners))
print("Unique ID's in integer representation: ", filteredUniqueOwners, "\nNumber of owner id's: ", len(filteredUniqueOwners), "\n")

# 3.       Count number of question per tag ( + get top category )
sortedTags = tagDataset.groupby(["Tag"]).size() #count how many in each "group: "Tag" "
sortByTop = sortedTags.sort_values(ascending=False) #sort to show top categories
print("Question 3: Count number of question per tag ( + get top category )")
print("Tags sorted from most used to least used: \n", sortByTop, "\n")

# 4.       get number of question asked by each owner / and in each category (same for answers dataset)
sortedQs = qDataset.groupby(["OwnerUserId"]).size()
print("Question 4: Get number of question asked by each owner / and in each category\n")
print(sortedQs, "\n")
#  answers datasheet
sortedAns = aDataset.groupby(["ParentId"]).size()
print("Question 4: Get number of questions answered by each owner / and in each category\n")
print(sortedAns, "\n")

# 5.       count Number of questions per day
format = "%Y-%m-%d"
dates = pd.DataFrame(pd.to_datetime(qDataset["CreationDate"]).dt.strftime(format))
sortedDates = dates.groupby(["CreationDate"]).size()
print("Question 5: Count Number of questions per day\n")
print(sortedDates, "\n")

# 6.       Count number of questions in each tags per day


# 7.       get the top ownerId answering in each tags


# 8.       number of answers per question


#9.       Find the questions which are still not answered?
unanswered = qDataset[~qDataset["Id"].isin(aDataset["ParentId"])]
print("Question 5: Find the questions which are still not answered\n")
print(unanswered)