import dash
from dash import html, dcc 
import plotly.express as px
from dash.dependencies import Input, Output, State
from apps import navigation
from main import *

tags={}
previous_list={}
ids={}


df=pd.read_csv("Dataset\Tags.csv")
df=df.fillna('')
id_column=df.iloc[:, 0].tolist()
tag_column=df.iloc[:,1].tolist()

def search_tags(input_tag):
 
 if input_tag is not None :
    unique_tags=[]
    for i in tag_column:
     if(input_tag in i):
       if i not in unique_tags:
           unique_tags.append(i)
     if len(unique_tags)==10:
           break 
    return unique_tags
 else:
    return {}

def search_id(input_tag):
 id_list=[]
 if input_tag is not None: 
   filtered_df = df[df['Tag'] == input_tag]
   id_list = filtered_df['id'].tolist()
   return id_list
 else:
    return {}

df=pd.read_csv("Dataset\EngineersDataset.csv")
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


admin_layout=html.Div([
html.Div([

       html.Div([
    html.Div(
        dcc.Input(
            id='search-box',
            type='text',
            placeholder='Search tags...',
            style={
                'margin-right': '20px',
                'padding': '10px',
                'border': '1px solid #ccc',
                'border-radius': '5px',
                'font-size': '16px',
                'width': '300px'
            }
        ),
        style={'display': 'inline-block'}
    ),
    html.Div(
        html.Div(
            dcc.Dropdown(
                id='tag-dropdown',
                options=[],
                placeholder='Select tags...',
                style={'width': '100%'}
            ),
            style={'width': '300px'}
        ),
        style={'display': 'inline-block'}
    )
],
style={
    'display': 'flex',
    'justify-content': 'center',
    'align-items': 'center',
    'margin-bottom': '20px'
}),
]),

html.Div([
   "The ID of the the person who can answer the quesiton shows below:",
   
],style={'background-color':'rgb(173, 216, 230)','width':'100%','height':'600px','border-radius':'10px','font-size':'30px','text-align': 'center','color':'black'}),

html.Div(
   [
   dash_table.DataTable(
    id='idtable',
    columns=[
        {'name': 'Id', 'id': 'Id', 'type': 'text', 'presentation': 'markdown'},
         {'name': 'Name', 'id': 'Name', 'type': 'text', 'presentation': 'markdown'},
        {'name': 'E-mail', 'id': 'E-mail', 'type': 'text', 'presentation': 'markdown'},
        {'name': 'Location', 'id': 'Location', 'type': 'text', 'presentation': 'markdown'},
        {'name': 'Status', 'id': 'Status', 'type': 'text', 'presentation': 'markdown'}
    ],
    style_table={
        'height': '500px',
        'overflowY': 'scroll',
        'border': 'thin lightgrey solid'
    },
    style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold',
        'border': 'thin lightgrey solid'
    },
    style_cell={
        'minWidth': '0px',
        'maxWidth': '250px',
        'whiteSpace': 'normal',
        'fontSize': '15px',
        'height': 'auto',
        'textAlign': 'left',
        'border': 'thin lightgrey solid'
    },
    page_size=30,
    page_action='none',
    sort_action='none',
    filter_action='none',
    
),
   
   ],style={'justify-content': 'center', 'align-items': 'center', 'margin-top': '-550px','width':'80%'}
)

 ]
)

@app.callback(
     Output('idtable','data'),
     [Input('tag-dropdown','value')]
)
def updateid(value):
   if value is not None:
      ids=search_id(value)
      data=[]
      for id in ids:
         result=find_id(id)
         if result != {}:
          data.append(result)
          print(data)
     
      return data
   
   else:
      return []




@app.callback(
    Output('tag-dropdown', 'options'),
    Input('search-box', 'value')
)
def update_tag(value):
 if value is not None:
    tags=search_tags(value)
    data= [{'label': tag, 'value': tag} for tag in tags]
    return data
 else:
    return []
