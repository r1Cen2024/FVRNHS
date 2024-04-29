# Usual Dash dependencies
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
import base64
from dash.exceptions import PreventUpdate
# Let us import the app object in case we need to define
# callbacks here
from app import app

navlink_style = {
    'color': '#fff'
}

CONTACT_STYLE = {
    # "position": "fixed",
    "bottom": "0em",
    "left": "0em",
    "right": "0em",
    "padding": "1em 1em",
    "background-color": "#24306E",
    "color": "#fff"
}

fvrnhslogo_loc = 'static/logofin.png'
encoded_image_fvrnhslogo = base64.b64encode(open(fvrnhslogo_loc, 'rb').read())

fblogo_loc = 'static/fblogo.png'
encoded_image_fblogo = base64.b64encode(open(fblogo_loc, 'rb').read())

# CSS Styling for the NavLink components
navbar = html.Div(
    dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='data:image/png;base64,{}'.format(encoded_image_fvrnhslogo.decode()),
                                        style={'height':'70px'}),
                                style={'padding':'4px 8px', 'z-index':'1'}),
                    ],
                    align="center",
                    className = 'g-0' #remove gutters (i.e. horizontal space between cols)
                ),
                href="/home",
            ),
            dbc.NavLink("Home", href="/home", style=navlink_style),
            dbc.NavLink("Announcements", href="/announcements", style=navlink_style),
            dbc.NavLink("Trends", href="/trends", style=navlink_style),
            dbc.NavLink("FAQs", href="/faqs", style=navlink_style),
            dbc.NavLink("Contact Us", href="/contactus", style=navlink_style),
            dbc.Button("Login", color="success", className="ms-auto", href="/login")
        ],
        dark=True,
        color='dark'
    )
)


navbarlogin = html.Div(
    dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='data:image/png;base64,{}'.format(encoded_image_fvrnhslogo.decode()),
                                        style={'height':'70px'}),
                                style={'padding':'4px 8px', 'z-index':'1'}),
                    ],
                    align="center",
                    className = 'g-0' #remove gutters (i.e. horizontal space between cols)
                ),
                href="/home",
            ),
            dbc.DropdownMenu(
                label = "Main Menu",
                children=[
                    dbc.DropdownMenuItem("Home", href='/home'),
                    dbc.DropdownMenuItem("Announcements", href='/announcements'),
                    dbc.DropdownMenuItem("Trends", href='/trends'),
                    dbc.DropdownMenuItem("FAQs", href='/faqs'),
                    dbc.DropdownMenuItem("Contact Us", href='/contactus'),
                ],
                style={'padding':'4px 8px', 'z-index':'1'},
                color='dark'
            ),
            dbc.DropdownMenu(
                label = "Pre-Enrollment",
                children=[
                    dbc.DropdownMenuItem("View Document Submission Details", href='/student/doc_submission'),
                ],
                style={'padding':'4px 8px', 'z-index':'1'},
                color='dark'
            ),
            dbc.DropdownMenu(
                label = "Enrollment",
                children=[
                    dbc.DropdownMenuItem("View Enrollment Instructions", href='/enrollinquiry'),
                    dbc.DropdownMenuItem("Fill Up Enrollment Form", href='/student/enrollment'),
                ],
                style={'padding':'4px 8px', 'z-index':'1'},
                color='dark'
            ),
            dbc.DropdownMenu(
                label = "Requests",
                children=[
                    dbc.DropdownMenuItem("Submit Document Request", href='/student/request'),
                    dbc.DropdownMenuItem("Check Ongoing Requests", href='/student/ongoingrequest'),
                ],
                style={'padding':'4px 8px', 'z-index':'1'},
                color='dark'
            ),
            dbc.DropdownMenu(
                label = "Admin Requests",
                children=[
                    dbc.DropdownMenuItem("Update Request Status", href='/admin/document_status'),
                    dbc.DropdownMenuItem("Add New Request", href='/admin/request'),
                ],
                style={'padding':'4px 8px', 'z-index':'1'},
                color='dark'
            ),
            dbc.DropdownMenu(
                label = "Users",
                children=[
                    dbc.DropdownMenuItem("View List of Users", href='/admin/users'),
                    dbc.DropdownMenuItem("Register New Adviser", href='/admin/newuser_adviser'),
                    dbc.DropdownMenuItem("Register New Student", href='/admin/newuser_student'),
                ],
                style={'padding':'4px 8px', 'z-index':'1'},
                color='dark'
            ),
            dbc.Button("Logout", color="danger", className="ms-auto", href="/logout") 
        ],
        dark=True,
        color='dark'
    )
)

contacts = html.Div(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col("Copyright 2023"),
                    dbc.Col(html.A(
                                    html.Img(src='data:image/png;base64,{}'.format(encoded_image_fblogo.decode()),
                                     style={'height':'40px'}), 
                            style={'padding':'4px 8px', 'z-index':'1'}, href="https://www.facebook.com/FVRNHS300762"))
                ],
                align="center",
                className="g-0",
            ),
        )
    ],
    style=CONTACT_STYLE,
)