import hashlib

import dash_bootstrap_components as dbc
from dash import callback_context, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.H2('Ongoing Requests'),
        html.Hr(),
        html.H4('Search Document Requests'),
        html.Div(
            dbc.Form(
                dbc.Row(
                    [
                        dbc.Label("Student Number", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='ongoingreq_studnumfilter',
                                placeholder='Student Number'
                            ),
                            width=5
                        ),
                    ],
                    className = 'mb-3'
                )
            )
        ),
        html.Div(id='ongoingreq_requestlist')
    ]
)

@app.callback(
    [
        Output('ongoingreq_requestlist', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('ongoingreq_studnumfilter', 'value')
    ]
)
def ongoingreq_loadrequests(pathname, searchterm):
    if pathname == '/student/ongoingrequest':
        # 1. Obtain records from the DB via SQL
        sql = """ SELECT stud_no, doc_n, req_status
            FROM request r
            INNER JOIN docu d ON r.doc_no = d.doc_no
            WHERE (r.req_status = 'Processing' or r.req_status = 'For Pickup')
        """
        values = [] # blank since I do not have placeholders in my SQL
        cols = ['Student Number', 'Document', 'Status']

        if searchterm:
            sql+="AND r.stud_no = %s"
            values+=[f"{searchterm}"]
        df = db.querydatafromdatabase(sql, values, cols)
        
        if df.shape:

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
            hover=True, size='sm')
            return [table]
        else:
            return ["No records to display"]
    else:
        raise PreventUpdate