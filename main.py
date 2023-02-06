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
print("Question 1: Unique Tags")
print(uniqueTags, "\nNumber of tags: ", len(uniqueTags), "\n")

# 2.       get the list and count of unique ownerIds
qOwner = qDataset.loc[:, "OwnerUserId"]
aOwner = aDataset.loc[:, "OwnerUserId"]

owners = pd.concat([qOwner, aOwner]) #combine the 2 above lists
uniqueOwners = pd.unique(owners)    
print("Question 2: Unique Owner Id's:")
print(uniqueOwners, "\nNumber of owner id's: ", len(uniqueOwners), "\n")
# print(uniqueOwners.astype('int'), "\nNumber of owner id's: ", len(uniqueOwners), "\n")

# 3.       Count number of question per tag ( + get top category )
sortedTags = tagDataset.groupby(["Tag"]).size() #count how many in each "group: "Tag" "
sortedTags.sort_values(ascending=False) #sort to show top categories

# 4.       get number of question asked by each owner / and in each category (same for answers dataset)
sortedQs = qDataset.groupby(["OwnerUserId"]).size()
sortedQs
#  answers datasheet
sortedAns = aDataset.groupby(["ParentId"]).size()
sortedAns

# 5.       count Number of questions per day
# format = "%Y-%m-%d"
dates = pd.DataFrame(pd.to_datetime(qDataset["CreationDate"]).dt.strftime(format))
sortedDates = dates.groupby(["CreationDate"]).size()
sortedDates

# 6.       Count number of questions in each tags per day


# 7.       get the top ownerId answering in each tags


# 8.       number of answers per question


#9.       Find the questions which are still not answered?