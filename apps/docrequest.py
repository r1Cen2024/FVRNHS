# Usual Dash dependencies
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# Let us import the app object in case we need to define
# callbacks here
from app import app
#for DB needs
from apps import dbconnect as db

from urllib.parse import urlparse, parse_qs

#document table
table_header = [
    html.Thead(html.Tr([html.Th("Document"), html.Th("Preparation Time")]))
]

row1 = html.Tr([html.Td("Old Diploma"), html.Td("3-5 Working Days")])
row2 = html.Tr([html.Td("Certification of Graduation"), html.Td("3-5 Working Days")])
row3 = html.Tr([html.Td("Certification of Enrollment"), html.Td("3-5 Working Days")])
row4 = html.Tr([html.Td("SF10"), html.Td("3-5 Working Days")])
row5 = html.Tr([html.Td("F-137"), html.Td("3-5 Working Days")])

table_body = [html.Tbody([row1, row2, row3, row4, row5])]


layout = html.Div(
    [
        html.H2('Document Request Form'), # Page Header
        html.Hr(),
        html.Br(),
        html.Br(),
        html.P("Here are the list of documents available for request from the School Registrar and their estimated preparation time. "
                           "Please check the status of your request to confirm the availability of your documents prior "
                           "to going to the Office."),
        html.Br(),
        dbc.Table(table_header + table_body, bordered=True),
        html.Br(),
        html.Br(),
        html.H4("Submit a Request"),
 dbc.Alert(id='docrequest_alert', is_open=False), # For feedback purposes
        dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Label("Student Number", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='docrequest_studno',
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
                                id='docrequest_doc',
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
                                id='docrequest_reason',
                                placeholder='Reason',
                            ),
                            width=5,
                        )
                    ],
                    className = 'mb-3' 
                ),

            ]
        ),
          dbc.Button(
            'Submit Request',
            id='docrequest_submit',
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
                    ], id='docrequest_feedback_message'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/student/ongoingrequest' # Clicking this would lead to a change of pages
                    )
                )
            ],
            centered=True,
            id='docrequest_successmodal',
            backdrop='static', # Dialog box does not go away if you click at the background
        )
    ]
)


@app.callback(
    [
        # The property of the dropdown we wish to update is the
        # 'options' property
        Output('docrequest_doc', 'options')
    ],
    [
        Input('url', 'pathname')
    ]
)
def docrequest_populatedocuments(pathname):
    if pathname == '/student/request':
        sql = """
        SELECT doc_n as label, doc_no as value
        FROM docu
        """
        values = []
        cols = ['label', 'value']

        df = db.querydatafromdatabase(sql, values, cols)
        # The output must be a dictionary with the following structure
        # options=[
        #     {'label': "Factorial", 'value': 1},
        #     {'label': "Palindrome Checker", 'value': 2},
        #     {'label': "Greeter", 'value': 3},
        # ]

        document_options = df.to_dict('records')
        return [document_options]
    else:
        # If the pathname is not the desired,
        # this callback does not execute
        raise PreventUpdate


@app.callback(
    [
        # dbc.Alert Properties
        Output('docrequest_alert', 'color'),
        Output('docrequest_alert', 'children'),
        Output('docrequest_alert', 'is_open'),
        # dbc.Modal Properties
        Output('docrequest_successmodal', 'is_open')
    ],
    [
        # For buttons, the property n_clicks 
        Input('docrequest_submit', 'n_clicks')
    ],
    [
        # The values of the fields are States 
        # They are required in this process but they 
        # do not trigger this callback
        State('docrequest_studno', 'value'),
        State('docrequest_doc', 'value'),
        State('docrequest_reason', 'value'),
    ]
)
def docrequest_requestsubmission(submitbtn, studentnum, document, reason):
    ctx = dash.callback_context
    # The ctx filter -- ensures that only a change in url will activate this callback
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'docrequest_submit' and submitbtn:
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
                alert_text = 'Check your inputs. Please enter your Student Number.'
            elif not document:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the Document.'
            elif not reason:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter reason for request.'
            else: # all inputs are valid
                # Add the data into the db

                sql = '''
                    INSERT INTO request (stud_no, doc_no,
                        req_reason, req_status)
                    VALUES (%s, %s, %s, %s)
                '''
                values = [studentnum, document, reason, 'Processing']

                db.modifydatabase(sql, values)

                # If this is successful, we want the successmodal to show
                modal_open = True

            return [alert_color, alert_text, alert_open, modal_open]

        else: # Callback was not triggered by desired triggers
            raise PreventUpdate

    else:
        raise PreventUpdate