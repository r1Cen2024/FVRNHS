import hashlib

import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.H2('Enter the details'),
        html.Hr(),
        dbc.Alert('Please check details.', color="danger", id='signup_alert',
                  is_open=False),
        dbc.Row(
            [
                dbc.Label("Username", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="signup_username", placeholder="Enter your username"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Password", width=2),
                dbc.Col(
                    dbc.Input(
                        type="password", id="signup_password", placeholder="Enter a password"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        
        dbc.Row(
            [
                dbc.Label(" Confirm Password", width=2),
                dbc.Col(
                    dbc.Input(
                        type="password", id="signup_passwordconf", placeholder="Re-type the password"
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Button('Sign up', color="secondary", id='signup_signupbtn'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("New Password")),
                dbc.ModalBody("Password has been created", id='signup_confirmation'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", href='/'
                    )
                ),
            ],
            id="signup_modal",
            is_open=False,
        ),
    ]
)


# disable the signup button if passwords do not match
@app.callback(
    [
        Output('signup_signupbtn', 'disabled'),
    ],
    [
        Input('signup_password', 'value'),
        Input('signup_passwordconf', 'value'),
    ]
)
def deactivatesignup(password, passwordconf):
    
    # enable button if password exists and passwordconf exists 
    #  and password = passwordconf
    enablebtn = password and passwordconf and password == passwordconf

    return [not enablebtn]


# To save the user
@app.callback(
    [
        Output('signup_alert', 'is_open'),
        Output('signup_modal', 'is_open'),   
    ],
    [
        Input('signup_signupbtn', 'n_clicks')
    ],
    [
        State('signup_username', 'value'),
        State('signup_password', 'value')
    ]
)
def saveuser(loginbtn, username, password):
    openalert = openmodal = False
    if loginbtn:
        if username and password:
            sql = """SELECT user_no, user_name
            FROM users
            WHERE 
                user_name = %s"""
            values = [username]
            cols = ['userid', 'username']
            df = db.querydatafromdatabase(sql, values, cols)
            
            if df.shape[0]: # if query returns rows
                sql = """UPDATE users
                    SET user_password = %s
                    WHERE user_name = %s"""  
                
                # This lambda fcn encrypts the password before saving it
                # for security purposes, not even database admins should see
                # user passwords 
                encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()  
                
                values = [encrypt_string(password), username]
                db.modifydatabase(sql, values)
                
                openmodal = True
            else:
                openalert = True
        else:
            openalert = True
    else:
        raise PreventUpdate

    return [openalert, openmodal]