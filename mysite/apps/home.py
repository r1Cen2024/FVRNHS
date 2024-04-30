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

# store the layout objects into a variable named layout
layout = html.Div(
    [
        html.Br(),
        html.H1('Study at FVRNHS'),
        html.H1('and achieve your dreams'),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Button("Enrollment Instructions", color="success", href='/enrollinquiry'),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Div(
            dbc.Container(
                [
                    html.H2("About FVRNHS", className="ms-auto"),
                    html.P("Established in Brgy. FVR, Norzagaray, Bulacan, 3013 in 1999, "),
                    html.P("the FVR National High School (FVRNHS) is a public high school that "),
                    html.P("is open to Junior High School (JHS) students. Currently, a total of 1129 "),
                    html.P("JHS students are enrolled in the school. There are also a total of 56 faculty "),
                    html.P("members, three administrative assistants, and one principal who work towards "),
                    html.P("providing the students with proper education and support for learning. "),
                    html.P("The school also has a total of four offices including the Principal’s "),
                    html.P("Office, Registrar’s Office, Accounting Office, and Guidance Office to "),
                    html.P("assist the students in their administrative needs.")
                ],
                fluid=True,
                className="py-3",
            ),
            className="p-3 bg-light rounded-3",
        )
    ]
)
