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

layout = html.Div(
    [
        html.H2('Enrollment Form'), # Page Header
        html.Hr(),
        html.Br(),
        html.Br(),
 dbc.Alert(id='enrollment_alert', is_open=False), # For feedback purposes
        dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Label("School Year", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='enrollment_sy',
                                placeholder="School Year"
                            ),
                            width=5
                        )
                    ],
                    className = 'mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Grade Level", width=1),
                        dbc.Col(
                            dcc.Dropdown(
                                ['7', '8', '9', '10'],
                                id='enrollment_grade',
                                placeholder='Grade Level'
                            ),
                            width=5
                        )
                    ],
                    className = 'mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Learner Reference No. (LRN)", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='enrollment_lrn',
                                placeholder="LRN"
                            ),
                            width=5
                        )
                    ],
                    className = 'mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Last Name", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='enrollment_ln',
                                placeholder="Last Name"
                            ),
                            width=5
                        )
                    ],
                    className = 'mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("First Name", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='enrollment_fn',
                                placeholder="First Name"
                            ),
                            width=5
                        )
                    ],
                    className = 'mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Middle Name", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='enrollment_mn',
                                placeholder="Middle Name"
                            ),
                            width=5
                        )
                    ],
                    className = 'mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Address", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='enrollment_add',
                                placeholder="Address"
                            ),
                            width=5
                        )
                    ],
                    className = 'mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Father's Name", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='enrollment_father',
                                placeholder="Father's Name"
                            ),
                            width=5
                        )
                    ],
                    className = 'mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Mother's Maiden Name", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='enrollment_mother',
                                placeholder="Mother's Maiden Name"
                            ),
                            width=5
                        )
                    ],
                    className = 'mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Guardian's Name", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='enrollment_guardian',
                                placeholder="Guardian's Name"
                            ),
                            width=5
                        )
                    ],
                    className = 'mb-3'
                ),
            ]
        ),
          dbc.Button(
            'Submit Form',
            id='enrollment_submit',
            n_clicks=0 # Initialize number of clicks
        ),
        dbc.Modal( # Modal = dialog box; feedback for successful saving.
            [
                dbc.ModalHeader(
                    html.H4('Form Submission')
                ),
                dbc.ModalBody(
                    [
                        'Form has been submitted.'
                    ], id='enrollment_feedback_message'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/home' # Clicking this would lead to a change of pages
                    )
                )
            ],
            centered=True,
            id='enrollment_successmodal',
            backdrop='static', # Dialog box does not go away if you click at the background
        )
    ]
)

@app.callback(
    [
        # dbc.Alert Properties
        Output('enrollment_alert', 'color'),
        Output('enrollment_alert', 'children'),
        Output('enrollment_alert', 'is_open'),
        # dbc.Modal Properties
        Output('enrollment_successmodal', 'is_open')
    ],
    [
        # For buttons, the property n_clicks 
        Input('enrollment_submit', 'n_clicks')
    ],
    [
        # The values of the fields are States 
        # They are required in this process but they 
        # do not trigger this callback
        State('enrollment_sy', 'value'),
        State('enrollment_grade', 'value'),
        State('enrollment_lrn', 'value'),
        State('enrollment_ln', 'value'),
        State('enrollment_fn', 'value'),
        State('enrollment_mn', 'value'),
        State('enrollment_add', 'value'),
        State('enrollment_father', 'value'),
        State('enrollment_mother', 'value'),
        State('enrollment_guardian', 'value'),
    ]
)
def enrollment_formsubmission(submitbtn, sy, grade, lrn, ln, fn, mn, add, father, 
                                 mother, guardian):
    ctx = dash.callback_context
    # The ctx filter -- ensures that only a change in url will activate this callback
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'enrollment_submit' and submitbtn:
            # the submitbtn condition checks if the callback was indeed activated by a click
            # and not by having the submit button appear in the layout

            # Set default outputs
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''

            # We need to check inputs
            if not sy: # If studentnum is blank, not studentnum = True
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter School Year.'
            elif not grade:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter Grade Level.'
            elif not lrn:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter LRN.'
            elif not ln:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter Last Name.'
            elif not fn:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter First Name.'
            elif not mn:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter Middle Name.'
            elif not add:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter Address.'
            elif not father:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Check your inputs. Please enter Father's Name."
            elif not mother:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Check your inputs. Please enter Mother's Name."
            elif not guardian:
                alert_open = True
                alert_color = 'danger'
                alert_text = "Check your inputs. Please enter Guardian's Name."
            else: # all inputs are valid
                # Add the data into the db

                sql = '''
                    INSERT INTO enrollment (enrollment_sy, enrollment_grade,
                       enrollment_lrn, enrollment_ln, enrollment_fn, enrollment_mn, enrollment_add,
                       enrollment_father, enrollment_mother, enrollment_guardian)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                values = [sy, grade, lrn, ln, fn, mn, add, father, mother, guardian]

                db.modifydatabase(sql, values)

                # If this is successful, we want the successmodal to show
                modal_open = True

            return [alert_color, alert_text, alert_open, modal_open]

        else: # Callback was not triggered by desired triggers
            raise PreventUpdate

    else:
        raise PreventUpdate