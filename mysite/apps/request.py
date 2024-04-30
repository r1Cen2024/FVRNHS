# Usual Dash dependencies
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import html

# Let us import the app object in case we need to define
# callbacks here
from app import app
#for DB needs
from apps import dbconnect as db

from urllib.parse import urlparse, parse_qs

#document table
layout = html.Div(
    [
        html.Div( # This div shall contain all dcc.Store objects
            [
                dcc.Store(id='request_toload', storage_type='memory', data=0),
            ]
        ),
        html.H2('Document Request Form'), # Page Header
        html.Br(),
        html.Br(),
        html.H4("Submit a Request"),
 dbc.Alert(id='request_alert', is_open=False), # For feedback purposes
        dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Label("Student Number", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='request_studno',
                                placeholder="Student Number"
                            ),
                            width=5
                        )
                    ],
                    className = 'mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Document", width=1),
                        dbc.Col(
                            dcc.Dropdown(
                                id='request_doc',
                                placeholder='Document'
                            ),
                            width=5
                        )
                    ],
                    className = 'mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Reason", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='request_reason',
                                placeholder='Reason',
                            ),
                            width=5,
                        )
                    ],
                    className = 'mb-3' 
                ),
                dbc.Row(
                    [
                        dbc.Label("Status", width=1),
                        dbc.Col(
                            dcc.Dropdown(
                                ['Processing', 'For Pickup', 'Completed'],
                                id='request_status',
                                placeholder='Status'
                            ),
                            width=5
                        )
                    ],
                    className = 'mb-3'
                ),

            ]
        ),
        dbc.Button(
            'Submit Request',
            id='request_submit',
            n_clicks=0 # Initialize number of clicks
        ),
        dbc.Modal( # Modal = dialog box; feedback for successful saving.
            [
                dbc.ModalHeader(
                    html.H4('Request Submission')
                ),
                dbc.ModalBody(
                    [
                        'Request has been submitted.'
                    ], id='request_feedback_message'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/admin/document_status', # Clicking this would lead to a change of pages
                        id = 'request_btn_modal'
                    )
                )
            ],
            centered=True,
            id='request_successmodal',
            backdrop='static', # Dialog box does not go away if you click at the background
        )
    ]
)

@app.callback(
    [
        # The property of the dropdown we wish to update is the
        # 'options' property
        Output('request_doc', 'options'),
        Output('request_toload', 'data'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search') # add this search component to the State
    ]
)

def request_loaddropdown(pathname, search):
    if pathname == '/admin/request':
        sql = """
            SELECT doc_n as label, doc_no as value
            FROM docu
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        document_options = df.to_dict('records')

        # are we on add or edit mode?
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
    else:
        raise PreventUpdate
    return [document_options, to_load]

@app.callback(
    [
        # Our goal is to update values of these fields
        Output('request_studno', 'value'),
        Output('request_doc', 'value'),
        Output('request_reason', 'value'),
        Output('request_status', 'value'),
    ],
    [
        # Our trigger is if the dcc.Store object changes its value
        # This is how you check a change in value for a dcc.Store
        Input('request_toload', 'modified_timestamp')
    ],
    [
        # We need the following to proceed
        # Note that the value of the dcc.Store object is in
        # the ‘data’ property, and not in the ‘modified_timestamp’ property
        State('request_toload', 'data'),
        State('url', 'search'),
    ]
)
def request_loadrequest(timestamp, toload, search):
    if toload: # check if toload = 1
        # Get id value from the search parameters
        parsed = urlparse(search)
        reqno = parse_qs(parsed.query)['id'][0]
        # Query from db
        sql = """
            SELECT stud_no, doc_no, req_reason, req_status
            FROM request
            WHERE req_no = %s
        """
        values = [reqno]
        col = ['request_studno', 'request_doc', 'request_reason', 'request_status']
        df = db.querydatafromdatabase(sql, values, col)
        request_studno = df['request_studno'][0]
        # Our dropdown list has the genreids as values then it will
        # display the correspoinding labels
        request_doc = int(df['request_doc'][0])
        request_reason = df['request_reason'][0]
        request_status = df['request_status'][0]
        return [request_studno, request_doc, request_reason, request_status]
    else:
        raise PreventUpdate


@app.callback(
    [
        # dbc.Alert Properties
        Output('request_alert', 'color'),
        Output('request_alert', 'children'),
        Output('request_alert', 'is_open'),
        # dbc.Modal Properties
        Output('request_successmodal', 'is_open'),
        Output('request_feedback_message', 'children'),
        Output('request_btn_modal', 'href'),
    ],
    [
        # For buttons, the property n_clicks 
        Input('request_submit', 'n_clicks'),
        Input('request_btn_modal', 'n_clicks'),
    ],
    [
        # The values of the fields are States 
        # They are required in this process but they 
        # do not trigger this callback
        State('request_studno', 'value'),
        State('request_doc', 'value'),
        State('request_reason', 'value'),
        State('request_status', 'value'),
        State('url', 'search')
    ]
)
def request_requestsubmission(submitbtn, closebtn, studentnum, document, reason, status, search):
    ctx = dash.callback_context
    # The ctx filter -- ensures that only a change in url will activate this callback
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'request_submit' and submitbtn:
            # the submitbtn condition checks if the callback was indeed activated by a click
            # and not by having the submit button appear in the layout

            # Set default outputs
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''

            # We need to check inputs
            if not studentnum: # If studentnum is blank, not studentnum = True
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter Student Number.'
            elif not document:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the Document.'
            elif not reason:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter reason for request.'
            elif not status:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please pick status.'
            else: # all inputs are valid
                # Add the data into the db
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]
                if create_mode == 'add':
                    sql = '''
                        INSERT INTO request (stud_no, doc_no,
                            req_reason, req_status)
                        VALUES (%s, %s, %s, %s)
                    '''
                    values = [studentnum, document, reason, status]

                    db.modifydatabase(sql, values)

                    feedbackmessage='Request has been submitted.'
                    okay_href='/admin/document_status'
                    # If this is successful, we want the successmodal to show
                    modal_open = True
                elif create_mode == 'edit':
                    parsed = urlparse(search)
                    reqno = parse_qs(parsed.query)['id'][0]
                    # 2. we need to update the db
                    sqlcode = """UPDATE request
                    SET
                        stud_no = %s,
                        doc_no = %s,
                        req_reason = %s,
                        req_status = %s
                    WHERE
                        req_no = %s
                    """
                    values = [studentnum, document, reason, status, reqno]
                    db.modifydatabase(sqlcode, values)
                    feedbackmessage = "Request has been updated."
                    okay_href = '/admin/document_status'
                    modal_open = True

                else:
                    raise PreventUpdate
            return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]

        else: # Callback was not triggered by desired triggers
            raise PreventUpdate

    else:
        raise PreventUpdate