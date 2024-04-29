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
    'Official transcripts from your previous school',
    'Birth Certificate',
    'Certification of Moral Conduct'
]

# store the layout objects into a variable named layout
layout = html.Div(
    [
        html.Div(
            dbc.Container(
                [
                    html.H1("Frequently Asked"),
                    html.H1("Questions"),
                    html.Br(),
                    html.Br(),
                    html.H4("1. What are your school's admission requirements?" ),
                    html.P("Admission requirements vary depending on the specific program or grade level "
                           "you are interested in. However, some general requirements may include:"),
                    html.Ul(children=[html.Li(i) for i in requirements]),
                    html.Br(),
                    html.H4("2. Can students transfer within the school year?"),
                    html.P("Students may be allowed to transfer within the school year on a case-to-case basis. Kindly"
                           "coordinate with the school registrar regarding this."),
                    html.Br(),
                    html.H4("3. What is the average class size?"),
                    html.P("The average class size at our school is 37-40 students." ),
                    html.Br(),
                ],
                fluid=True,
                className="py-3",
            ),
            className="p-3 bg-light rounded-3",
        )
    ]
)
