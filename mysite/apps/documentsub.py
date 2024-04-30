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

layout = html.Div(
    [
        html.H2('Pre-Enrollment Module'), # Page Header
        html.Hr(),
        html.Br(),
        html.Br(),
        html.H4("Document Submission Instructions"),
        html.Br(),
        html.Br(),
        html.P("Here are the required documents to be submitted to the School Registrar's Office as Hard"),
        html.Br(),
        html.P("New Students" ,style={'fontWeight': 'bold'}),
        html.P("1.Completed Enrollment Form: The enrollment form is the primary document that gathers all the necessary",
               "information about the student, including their personal details, academic history, and emergency contact information."),
        html.P("2.Birth Certificate: A copy of the students Birth Certificate is Required to verify their age and identity."),
        html.P("3.Proof of Residency: Proof of residency may include a utility bill, lease agreement, or property tax statement. This "
               "document is needed to ensure that the student lives within the school attendance boundaries."),
        html.P("4.Immunization Records: Up-to-date immunization are required to ensure that the student is compliant with state and school immunization requirements."),
        html.P("5.Previous School Records: If a student is transfering from another school, their previous school records including transcripts, attendance"
               "records, and disciplinary records, may be requested."),
        html.P("6.Standardized test Score: Some schools may require standardized test scores such as the SAT or ACT, for admission purposes."),
        html.P("7.Health and Medical Records: If the student has any special health needs, they may be required to provide additional health and medical records."),
        html.P("8.Emergency contact information: The school will need emergency contact information in case of an accident or illness."),
        html.Br(),
        html.P("Eisting Students" ,style={'fontWeight': 'bold'}),
        html.P("1.Proof of residency: proof of residency may be required again to verify that the student still lives within school attendance boundaries."),
        html.P("2.Updated Immunization Records: Updated immunization recoreds may be requested to ensure the student is compliant with ongoing immunization requirements."),
        html.P("3.Health and Medical Records: Any updates to the students health or medical condistions should be provided to the school registrar."),
    ]
)