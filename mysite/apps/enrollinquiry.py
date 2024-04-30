# Usual Dash dependencies
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table

from dash.exceptions import PreventUpdate
import pandas as pd
# Let us import the app object in case we need to define
# callbacks here
from app import app

requirements = [
    'A completed application form',
    'Official transcripts from your previous school',
    'Standardized test scores (if applicable)',
    'Letters of recommendation',
    'A personal statement'
]

finaid = ['Grants', 'Scholarships', 'Loans', 'Work-Study Programs']

# store the layout objects into a variable named layout
layout = html.Div(
    [
        html.Div(
            dbc.Container(
                [
                    html.H1("Enroll With Us!"),
                    html.Br(),
                    html.Br(),
                    html.P("For interested parents and students, here are the instructions, enrollment "
                           "flowchart, list of required documents needed."),
                    html.Br(),
                    html.P("Please email 300762@deped.gov.ph for more details."),
                    html.Br(),
                    html.Br(),
                    html.H3("Enrollment Instructions"),
                    #Insert flowchart here.
                    html.P("1. For new students, submit requirements to school registrar." ),
                    html.P("2. Receive login credentials from registrar."),
                    html.P("2. Fill up enrollment form."),
                    html.P("3. Wait for approval by the registrar."),
                    html.Br(),
                    html.Br(),
                    html.H3("Required Documents and Forms"),
                    html.P("1. Official transcript from your previous school"),
                    html.P("2. Birth Certificate"),
                    html.P("3. Certification of Moral Conduct"),
                ],
                fluid=True,
                className="py-3",
            ),
            className="p-3 bg-light rounded-3",
        )
    ]
)
