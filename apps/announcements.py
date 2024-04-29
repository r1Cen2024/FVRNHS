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

benefits = [
    'Priority placement in your desired classes',
    'Reduced stress levels throughout the year',
    'More time to focus on your studies',
    'A chance to make new friends and get to know your teachers'
]

# store the layout objects into a variable named layout
layout = html.Div(
    [
        html.Div(
            dbc.Container(
                [
                    html.H1("Announcements", className="ms-auto"),
                    html.P("Keep updated with the latest news" 
                    "and important announcements from the FVRNHS school administration."),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.H2("Early Enrollment at FVRNHS"),
                    html.P("Calling all new and old students!" 
                    "Enroll early for the next school year and get a head start on your education!"),
                    html.P("Benefits of early enrollment"),
                    html.Ul(children=[html.Li(i) for i in benefits]),
                    html.P("Don't miss out on this great opportunity."),
                    html.P("Enrol early today!"),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.H2("No Class Suspensions due to Strike"),
                    html.P("Calling all new and old students!" 
                    "Enroll early for the next school year and get a head start on your education!"),
                    html.P("Benefits of early enrollment"),
                    html.Ul(children=[html.Li(i) for i in benefits]),
                    html.P("Don't miss out on this great opportunity."),
                    html.P("Enrol early today!")
                ],
                fluid=True,
                className="py-3",
            ),
            className="p-3 bg-light rounded-3",
        )
    ]
)
