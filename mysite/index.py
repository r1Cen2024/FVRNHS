# Dash related dependencies
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
# To open browser upon running your app
import webbrowser
# Importing your app definition from app.py so we can use it
from app import app
from apps import home, announcements, faq, contactus, enrollinquiry, docrequest, login, signup, ongoingreq, userlist, docstatus, request
from apps import documentsub, newuser, newusertr, trends, enrollment
from apps import commonmodules as cm
from apps import dbconnect as db

CONTENT_STYLE = {
    "margin-top": "2em",
    "margin-bottom": "2em",
    "margin-left": "1em",
    "margin-right": "1em",
    "padding": "1em 1em",
}

app.layout = html.Div(
    [
        # Location Variable -- contains details about the url
        dcc.Location(id='url', refresh=True),

        # LOGIN DATA
        # 1) logout indicator, storage_type='session' means that data will be retained
        #  until browser/tab is closed (vs clearing data upon refresh)
        dcc.Store(id='sessionlogout', data=True, storage_type='session'),
        
        # 2) current_user_id -- stores user_id
        dcc.Store(id='currentuserid', data=-1, storage_type='session'),
        
        #Logged in Navbar
        html.Div(
            cm.navbarlogin,
            id='navbarlogin_div',
            className='d-none'
        ),

        #Logged out Navbar
        html.Div(
            cm.navbar,
            id='navbar_div'
        ),

        # Page Content -- Div that contains page layout
        html.Div(id='page-content', style=CONTENT_STYLE),
        cm.contacts,
    ]
)

@app.callback(
    [
        Output('page-content', 'children'),
        Output('sessionlogout', 'data'),
        Output('navbarlogin_div', 'className'),
        Output('navbar_div', 'className')
    ],
    [
        # If the path (i.e. part after the website name; 
        # in url = youtube.com/watch, path = '/watch') changes, 
        # the callback is triggered
        Input('url', 'pathname')
    ],
    [
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'),
    ]
)
def displaypage (pathname, sessionlogout, userid):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'url':
            if userid < 0: # if logged out
                if pathname == '/' or pathname == '/home':
                    # If we are at the homepage, let us output 'home'
                    returnlayout = home.layout
                elif pathname == '/announcements':
                    returnlayout = announcements.layout
                elif pathname == '/faqs':
                    returnlayout = faq.layout
                elif pathname == '/contactus':
                    returnlayout = contactus.layout
                elif pathname == '/enrollinquiry':
                    returnlayout = enrollinquiry.layout
                elif pathname == '/student/request':
                    returnlayout = 'Sorry you do not have access to this page.'
                elif pathname == '/login':
                    returnlayout = login.layout
                elif pathname == '/signup':
                    returnlayout = signup.layout
                elif pathname == '/student/ongoingrequest':
                    returnlayout = 'Sorry you do not have access to this page.'
                elif pathname == '/admin/users':
                    returnlayout = 'Sorry you do not have access to this page.'
                elif pathname == '/admin/document_status':
                    returnlayout = 'Sorry you do not have access to this page.'
                elif pathname == '/admin/request':
                    returnlayout = 'Sorry you do not have access to this page.'
                elif pathname == '/trends':
                    returnlayout = trends.layout
                elif pathname == '/admin/newuser_student':
                    returnlayout = 'Sorry you do not have access to this page.'
                elif pathname == '/admin/newuser_adviser':
                    returnlayout = 'Sorry you do not have access to this page.'
                elif pathname == '/student/doc_submission':
                    returnlayout = 'Sorry you do not have access to this page.'
                elif pathname == '/student/enrollment':
                    returnlayout = 'Sorry you do not have access to this page.'
                elif pathname == '/adviser/classlist':
                    returnlayout = 'Sorry you do not have access to this page.'
                else:
                    returnlayout = 'error404'
            
            else:    
                if pathname == '/logout':
                    returnlayout = login.layout
                    sessionlogout = True
                elif pathname == '/' or pathname == '/home':
                    # If we are at the homepage, let us output 'home'
                    returnlayout = home.layout
                elif pathname == '/announcements':
                    returnlayout = announcements.layout
                elif pathname == '/faqs':
                    returnlayout = faq.layout
                elif pathname == '/contactus':
                    returnlayout = contactus.layout
                elif pathname == '/enrollinquiry':
                    returnlayout = enrollinquiry.layout
                elif pathname == '/student/request':
                    returnlayout = docrequest.layout
                elif pathname == '/login':
                    returnlayout = login.layout
                elif pathname == '/admin/signup':
                    returnlayout = signup.layout
                elif pathname == '/student/ongoingrequest':
                    returnlayout = ongoingreq.layout
                elif pathname == '/admin/users':
                    returnlayout = userlist.layout
                elif pathname == '/admin/document_status':
                    returnlayout = docstatus.layout
                elif pathname == '/admin/request':
                    returnlayout = request.layout
                elif pathname == '/trends':
                    returnlayout = trends.layout
                elif pathname == '/admin/newuser_student':
                    returnlayout = newuser.layout
                elif pathname == '/admin/newuser_adviser':
                    returnlayout = newusertr.layout
                elif pathname == '/student/doc_submission':
                    returnlayout = documentsub.layout
                elif pathname == '/student/enrollment':
                    returnlayout = enrollment.layout
                elif pathname == '/adviser/classlist':
                    returnlayout = 'Sorry you do not have access to this page.'
                else:
                    returnlayout = 'error404'                
                
            # decide sessionlogout value
            logout_conditions = [
                pathname in ['/', '/logout'],
                userid == -1,
                not userid
            ]
            sessionlogout = any(logout_conditions)

            # hide logged in navbar if logged-out; else, set class/style to default
            navbarlogin_classname = 'd-none' if sessionlogout else ''

            navbar_classname = '' if sessionlogout else 'd-none'
        else:
            raise PreventUpdate
	
        return [returnlayout, sessionlogout, navbarlogin_classname, navbar_classname]
    else:
        raise PreventUpdate


if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', autoraise=False)
    app.run_server(debug=False)