from dash import html, dcc
from dash.dependencies import Input, Output, State
from apps import navigation
from main import app
import main

busy_users = [] # List to store user IDs with status 'Busy'

# Get the dataset
df = main.eDataset.copy()
print(df.head())

def updateUserStatus(inputUserID):
    print(inputUserID)
    inputUserID = float(inputUserID)
    rowIndexList = df.index[df['Ids'] == inputUserID].tolist()
    if len(rowIndexList) > 0:
        rowIndex = rowIndexList[0]

        if df.at[rowIndex, 'Status'] == 'Active':
            busy_users.append(inputUserID)
            df.at[rowIndex, 'Status'] = 'Busy'
        else:
            busy_users.remove(inputUserID)
            df.at[rowIndex, 'Status'] = 'Active'
        
        print(busy_users)
    else:
        print(f"No row found with ID {inputUserID}")


admin_layout=html.Div(
    children=[
        navigation.navbar,
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='first-name-filter', 
                    options=[
                        {'label':str(i), 'value':str(i)}
                        for i in main.uniqueFN],
                    value='',
                    placeholder="Search for first name..."
                )
            ], style={'flex': '1', 'margin':'0.4rem'}),
            html.Div([
                dcc.Dropdown(
                    id='last-name-filter', 
                    options=[
                        {'label':str(i), 'value':str(i)}
                        for i in main.uniqueLN],
                    value='', 
                    placeholder="Search for surname..."
                )
            ], style={'flex': '1', 'margin':'0.4rem'}),
            html.Div([
                dcc.Dropdown(
                    id='status-filter', 
                    options=[
                        {'label': 'All', 'value': 'all'},
                        {'label': 'Active', 'value': 'Active'},
                        {'label': 'Busy', 'value': 'Busy'}
                    ], 
                    value='all',
                )
            ], style={'flex': '1', 'margin':'0.4rem'}),
            html.Button(
                'Search',
                className="userBtn",
                type="submit",
                id="searchButton",
                n_clicks=0,
                style={'flex': '1', 'margin':'0.4rem'}),
        ], 
        style={'display': 'flex', 'margin':'2rem'}),

        html.Div(
            className="adminRow",
            children=[
                html.Div(
                    className="resultsColumn",
                    children=[
                        html.Div(
                            id='results',
                            className="userResults",
                            children=[
                        
                            ]
                        ),
                    ]
                ),
                html.Div(
                    className="updateColumn",
                    children=[
                        html.Div(
                            id='updateUsers',
                            className="updateUserStatus",
                            children=[
                                html.Div(
                                    className="updateDiv",
                                    children=[
                                        html.H2("Update a users status below", className="updateTitle"),
                                        html.Div(
                                            className="id-search-bar",
                                            children=[
                                                dcc.Input(
                                                    placeholder="Search by ID...",
                                                    type="text",
                                                    value="",
                                                    id="userInput",
                                                    className="idInput"
                                                ),
                                                html.Button(
                                                    'Update',
                                                    className="updateBtn",
                                                    type="Update",
                                                    id="updateButton",
                                                    n_clicks=0,
                                                ),
                                                html.P(id='confirmStatus')
                                            ]
                                        ),
                                    ]
                                )
                            ]
                        ),
                    ]
                ), 
            ] 
        )  
    ]
)

@app.callback(
    Output('results', 'children'),
    Input('searchButton', 'n_clicks'),
    State('first-name-filter', 'value'),
    State('last-name-filter', 'value'),
    State('status-filter', 'value'),
    prevent_initial_call=True
)
def filter_data(n_clicks, first_name, last_name, status):
    global df
    # Apply filters based on selected values
    if first_name:
        df = df[df['FirstName'] == first_name]
    if last_name:
        df = df[df['LastName'] == last_name]
    if status != 'all':
        df = df[df['Status'] == status]

    # Create a list of div elements, one for each row in the filtered dataset
    divs = []
    for i, row in df.iterrows():
        div = html.Div([
            html.P(f"ID: {row['Ids']}"),
            html.P(f"Name: {row['FirstName']} {row['LastName']}"),
            html.P(f"Email: {row['Email']}"),
            html.P(f"Job Title: {row['JobTitle']}"),
            html.P(f"Address: {row['Address']}"),
            html.P(f"Status: {row['Status']}"),
            html.Hr()
        ])
        divs.append(div)

    # Return the list of div elements
    return divs

@app.callback(
    Output(component_id='confirmStatus', component_property='children'),
    [Input(component_id='updateButton', component_property='n_clicks')],
    [State(component_id='userInput', component_property='value')],
    prevent_initial_call=True
)
def updateStatus(n, inputID):
    print(inputID)
    updateUserStatus(inputID)
    return "Status has been changed"