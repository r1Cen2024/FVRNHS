import hashlib

import dash_bootstrap_components as dbc
from dash import callback_context, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from urllib.parse import urlparse, parse_qs

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.H2('Document Requests'),
        html.Hr(),
        html.Div( # Create section to show list of movies
            [
                html.Div( # Add Movie Btn
                            [
                                # Add movie button will work like a
                                # hyperlink that leads to another page
                                dbc.Button(
                                    "Add Document Request",
                                    href='/admin/request?mode=add'
                                )
                            ]
                        ),
                        html.Hr(),
                html.H4('Search Document Requests'),
                html.Div(
                    dbc.Form(
                        dbc.Row(
                            [
                                dbc.Label("Search Status", width=1),
                                dbc.Col(
                                    dbc.Input(
                                        type='text',
                                        id='docstatus_statusfilter',
                                        placeholder='Request Status'
                                    ),
                                    width=5
                                )
                            ],
                            className = 'mb-3'
                        )
                    )
                ),
                html.Div(
                    id='docstatus_list'
                )
            ]
        )
    ]
)

@app.callback(
    [
        Output('docstatus_list', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('docstatus_statusfilter', 'value'),
    ]
)
def docstatus_loadlist(pathname, searchterm):
    if pathname == '/admin/document_status':
        # 1. Obtain records from the DB via SQL
        sql = """ SELECT stud_no, doc_n, req_status, req_no
            FROM request r
            INNER JOIN docu d ON r.doc_no = d.doc_no
        """
        values = [] # blank since I do not have placeholders in my SQL
        cols = ['Student Number', 'Document', 'Status', "ID"]

        if searchterm:
            # We use the operator ILIKE for pattern-matching
            sql += 'AND req_status ILIKE %s'
            # The % before and after the term means that
            # there can be text before and after
            # the search term
            values += [f"%{searchterm}%"]

        df = db.querydatafromdatabase(sql, values, cols)
        # 2. Create the html element to return to the Div

        if df.shape: # check if query returned anything
            buttons = []
            for req_no in df['ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit',
                            href=f'/admin/request?mode=edit&id={req_no}',
                            size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                ]
            df['Action'] = buttons
            # remove the column ID before turning into a table
            df = df[['Student Number', 'Document', 'Status', "Action"]]
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                hover=True, size='sm')
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate