from dash import html, dcc
from dash.dependencies import Input, Output, State
from apps import navigation
from main import app
import main

# Get the dataset
Ogdf = main.eDataset.copy()
# print(df.head())

def updateUserStatus(inputUserID):
    print(inputUserID)
    inputUserID = float(inputUserID)
    rowIndexList = Ogdf.index[Ogdf['Ids'] == inputUserID].tolist()
    if len(rowIndexList) > 0:
        rowIndex = rowIndexList[0]

        if Ogdf.at[rowIndex, 'Status'] == 'Active':
            main.busy_users.append(inputUserID)
            Ogdf.at[rowIndex, 'Status'] = 'Busy'
        else:
            main.busy_users.remove(inputUserID)
            Ogdf.at[rowIndex, 'Status'] = 'Active'
        
        print(main.busy_users)
    else:
        print(f"No row found with ID {inputUserID}")


admin_layout=html.Div(
    children=[
        navigation.navbar,
        html.Div(
            className="dropdownDiv",
            children=[
                html.Div([
                    dcc.Dropdown(
                        id='first-name-filter', 
                        options=[
                            {'label':str(i), 'value':str(i)}
                            for i in main.uniqueFN],
                        value='Michael',
                        placeholder="Search for first name..."
                    )
                ], style={'flex': '1', 'margin':'0.5rem'}),
                html.Div([
                    dcc.Dropdown(
                        id='last-name-filter', 
                        options=[
                            {'label':str(i), 'value':str(i)}
                            for i in main.uniqueLN],
                        value='Villa', 
                        placeholder="Search for surname..."
                    )
                ], style={'flex': '1', 'margin':'0.5rem'}),
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
                ], style={'flex': '1', 'margin':'0.5rem'}),
                html.Button(
                    'Search',
                    className="adminSearchBtn",
                    type="submit",
                    id="searchButton",
                    n_clicks=0,
                    style={'flex': '1', 'margin':'0.5rem'}
                ),
            ], 
            style={'display': 'flex', 'margin':'2rem'}
        ),

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
                                        html.H2("Update Status", className="updateTitle"),
                                        html.Img(
                                            className="statusImg",
                                            src="assets\Status.png"
                                        ),
                                        html.Div(
                                            className="id-search-bar",
                                            children=[
                                                html.Div(
                                                    children=[
                                                        html.P(
                                                            className="statusChanger",
                                                            children=[
                                                                'Input a users ID to change their status'
                                                            ]
                                                        ),
                                                        dcc.Input(
                                                            placeholder="Search by ID...",
                                                            type="text",
                                                            value="",
                                                            id="userInput",
                                                            className="idInput"
                                                        )
                                                    ]
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
    prevent_initial_call=False
)
def filter_data(n_clicks, first_name, last_name, status):
    df = Ogdf.copy()
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
        div = html.Div(
        className="userCard",
        children=[
            html.P(f"ID: {row['Ids']}"),
            html.P(f"Name: {row['FirstName']} {row['LastName']}"),
            html.P(f"Email: {row['Email']}"),
            # html.P(f"Job Title: {row['JobTitle']}"),
            html.P(f"Address: {row['Address']}"),
            html.P(f"Status: {row['Status']}"),
        ])
        divs.append(div)

    # Return the list of div elements
    return  html.Div(
                className="cardGrid",
                children=divs
            ) 

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