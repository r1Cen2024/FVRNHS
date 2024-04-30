import hashlib

import dash_bootstrap_components as dbc
from dash import callback_context, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db
from apps import docrequest


tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div(id='userlist_teacher', className="card-text"),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div(id='userlist_student', className="card-text"),
        ]
    ),
    className="mt-3",
)


layout = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Teachers", tab_id="tab-1"),
                dbc.Tab(label="Students", tab_id="tab-2"),
            ],
            id="tabs",
            active_tab="tab-1",
        ),
        html.Div(id="content"),
    ]
)

@app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return tab1_content
    elif at == "tab-2":
        return tab2_content
    return html.P("This shouldn't ever be displayed...")

@app.callback(
    [
        Output('userlist_teacher', 'children'),
    ],
    [
        Input('url', 'pathname')
    ]
)
def userlist_loadteachers(pathname):
    if pathname == '/admin/users':
        # 1. Obtain records from the DB via SQL
        sql = """ SELECT faculty_fn, faculty_mn, faculty_ln
            FROM adviser
        """
        values = [] # blank since I do not have placeholders in my SQL
        cols = ['First Name', 'Middle Name', 'Last Name']
        df = db.querydatafromdatabase(sql, values, cols)
        # 2. Create the html element to return to the Div
        table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
        hover=True, size='sm')
        return [table]
    else:
        raise PreventUpdate
    

@app.callback(
    [
        Output('userlist_student', 'children'),
    ],
    [
        Input('url', 'pathname')
    ]
)
def userlist_loadusers(pathname):
    if pathname == '/admin/users':
        # 1. Obtain records from the DB via SQL
        sql = """ SELECT stud_fn, stud_mn, stud_ln
            FROM student
        """
        values = [] # blank since I do not have placeholders in my SQL
        cols = ['First Name', 'Middle Name', 'Last Name']
        df = db.querydatafromdatabase(sql, values, cols)
        # 2. Create the html element to return to the Div
        table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
        hover=True, size='sm')
        return [table]
    else:
        raise PreventUpdate
    
