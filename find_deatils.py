import pandas as pd

df=pd.read_csv("/Users/zouweijian/Desktop/dataset/dataset/EngineersDataset.csv")
df=df.fillna('')

id_column = df.iloc[:,0].to_list()
firstName_column=df.iloc[:,1].to_list()
LastName_column=df.iloc[:,2].tolist()
location_column=df.iloc[:,5].tolist()
email_column=df.iloc[:,3].tolist()
Status_colum=df.iloc[:,6].tolist()


def find_id(input_id):
    if input_id in id_column:
       index = id_column.index(input_id) 
       output={'Id':id_column[index],'Name':firstName_column[index]+LastName_column[index],'E-mail':email_column[index],'Location':location_column[index],'Status':Status_colum[index]}
       print(output)
       return output
    else:
      return {}
    


