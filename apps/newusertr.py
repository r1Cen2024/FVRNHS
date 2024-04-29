import hashlib

import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db


# This page is for admin to register the username of the user 
# No passwords will be created here. User will sign up using the sign up page 
# to create a password for their account.

layout = html.Div(
    [
        html.H2('Enter the details'),
        html.Hr(),
        dbc.Alert('Please supply details.', color="danger", id='newusertr_alert',
                  is_open=False),
        dbc.Row(
            [
                dbc.Label("Faculty Number", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="newusertr_facultyno", placeholder="Enter Faculty Number"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Username", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="newusertr_username", placeholder="Enter username."
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Button('Register', color="secondary", id='newusertr_reg_btn'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("New User")),
                dbc.ModalBody("User has been registered.", id='newusertr_confirmation'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", href='/'
                    )
                ),
            ],
            id="newusertr_modal",
            is_open=False,
        ),
    ]
)


# disable the register button if passwords do not match
@app.callback(
    [
        Output('newusertr_reg_btn', 'disabled'),
    ],
    [
        Input('newusertr_username', 'value'),
    ]
)
def deactivateregistration(username):
    
    # enable button if password exists and passwordconf exists 
    #  and password = passwordconf
    enablebtn = username

    return [not enablebtn]


# To save the user
@app.callback(
    [
        Output('newusertr_alert', 'is_open'),
        Output('newusertr_modal', 'is_open')   
    ],
    [
        Input('newusertr_reg_btn', 'n_clicks')
    ],
    [
        State('newusertr_facultyno', 'value'),
        State('newusertr_username', 'value'),
    ]
)
def saveuser(loginbtn, facultyno, username):
    openalert = openmodal = False
    if loginbtn:
        if facultyno and username:
            sql = """INSERT INTO users (faculty_no, user_name)
            VALUES (%s, %s)"""  
            
            values = [facultyno, username]
            db.modifydatabase(sql, values)
            
            openmodal = True
        else:
            openalert = True
    else:
        raise PreventUpdate

    return [openalert, openmodal]