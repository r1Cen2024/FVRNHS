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
        html.Div(
            dbc.Container(
                [
                    html.H1("Contact Us"),
                    html.Br(),
                    html.Br(),
                    html.P("We are always happy to hear from you. Please feel free to contact us "
                           "with any questions, comments, or concerns."),
                    html.Br(),
                    html.P("General Inquiries"),
                    html.P("Email: 300762@deped.gov.ph"),
                    html.P("Mailing Address"),
                    html.P("Brgy. FVR, Norzagaray, Bulacan 3013"),
                    html.Br(),
                    html.P("Social Media Pages"),
                    html.P("Facebook: https://www.facebook.com/FVRNHS300762"),
                    html.Br(),
                    html.P("We look forward to hearing from you!"),
                ],
                fluid=True,
                className="py-3",
            ),
            className="p-3 bg-light rounded-3",
        )
    ]
)
