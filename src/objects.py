import dash_bootstrap_components as dbc
from dash import html

IMAGE = 'assets/1572594055044.png'

input_style={'background-color':'transparent','color':'white'}
small_input_style={'background-color':'transparent','color':'white'}
select_style={'background-color':'transparent','border-color':'red'}

packages = ['Access', 'Starter', 'Standard', 'Full-stack']

myButton = dbc.Button("Teklif Oluştur", id="submit", n_clicks=0, color='secondary', outline=True, disabled=True)

submit_button = dbc.Button("Login", id="verify", n_clicks=0, outline=True , color='secondary', className="me-1", style={'width':'15%'})

old_submit_button = dbc.Button("Giriş", id="verify", n_clicks=0,
                            style={'border-width': '0.625rem', 'font-size': '0.875rem', 'background-color': "#D6EAF8",
                                   'color': 'black', "width": "9.375rem"})


uploadStyle = {
    'width': '95%',
    'height': '60px',
    'lineHeight': '60px',
    'borderWidth': '2px',
    'borderStyle': 'dashed',
    'borderRadius': '5px',
    'color': '#44d9e8',
    'borderColor': '#44d9e8',
    'backgroundColor': 'rgba(0, 255, 0, 0.1)',
    'textAlign': 'center',
    'margin': '10px',
    'margin-left': '20px'
}

uploadStyle_green = {
    'width': '95%',
    'height': '60px',
    'lineHeight': '60px',
    'borderWidth': '2px',
    'borderStyle': 'dashed',
    'borderRadius': '5px',
    'color': 'green',
    'borderColor': 'green',
    'backgroundColor': 'rgba(0, 255, 0, 0.1)',
    'textAlign': 'center',
    'margin': '10px',
    'margin-left': '30px'
}

uploadStyle_red = {
    'width': '95%',
    'height': '60px',
    'lineHeight': '60px',
    'borderWidth': '2px',
    'borderStyle': 'dashed',
    'borderRadius': '5px',
    'borderColor': 'red',
    'backgroundColor': 'rgba(255, 0, 0, 0.1)',
    'textAlign': 'center',
    'margin': '10px',
    'margin-left': '30px'
}

uploadText_red = html.Div([
    'Drag and Drop or ',
    html.A('Select Files '),
    html.A('No Files Uploaded Yet !', style={'font-weight': 'bold'}),
])

uploadText_green = html.Div([
    'Drag and Drop or ',
    html.A('Select Files '),
    html.A('Files Successfully Uploaded !', style={'font-weight': 'bold'}),
])
