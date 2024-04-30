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


# store the layout objects into a variable named layout
layout = html.Div(
    [
        html.Div(
            dbc.Container(
                [
                    html.H1("Trends and Reports", className="ms-auto"),
                    html.P("See the latest enrollment Trends in" 
                    "FVRNHS."),
                    html.Br(),
                    html.H2("Enrollment Trends"),
                    html.H2("School in Numbers"),
                    html.P("Calling all new and old students!" 
                    "Enroll early for the next school year and get a head start on your education!"),
                    html.P("Benefits of early enrollment"),
                    html.Div(
                        id='numbers_table'
                    ),
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


@app.callback(
    [
        Output('numbers_table', 'children')
    ],
    [
        Input('url', 'pathname')
    ]
)
def trends_loadnumberlist(pathname):
    if pathname == '/trends':
        
        sql = """ SELECT COUNT (enrollment_no) as enrollee_total 
        FROM enrollment
        WHERE enrollment_sy = '2022-2023'
        """
        values = [] # blank since I do not have placeholders in my SQL
        cols = ['Total Number of Enrollees']
        df = db.querydatafromdatabase(sql, values, cols)

        table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
        hover=True, size='sm')

        return [table]


    else:
        raise PreventUpdate