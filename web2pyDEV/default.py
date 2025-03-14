# -*- coding: utf-8 -*- 
# Specifies the encoding for the Python file as UTF-8

from gluon import SQLFORM, URL, DIV, A, H2
# Import necessary components from the gluon framework, such as SQLFORM for database forms, URL for URL handling, DIV, A, and H2 for HTML elements

from gluon.tools import Auth
# Import the Auth class for user authentication features

# Initialize authentication system
auth = Auth(db)
auth.define_tables(username=False, signature=False)
# Set up the authentication system, defining tables for user management, but not including username or signature in the tables

def index():
    """ Home page: Displays ponds and rootstocks owned by the logged-in user. """
    if not auth.user:
        # If no user is logged in, return a page asking for login and empty sections
        return dict(message="Please log in", form=None, grid=None, rootstock_form=None, rootstock_grid=None, knotstock_list_grid=None)

    # ---- Ponds Section ----
    db.pond.created_by.default = auth.user.id
    # Set the default value of 'created_by' field to the logged-in user's ID
    db.pond.created_by.writable = False
    db.pond.created_by.readable = False
    # Make 'created_by' field neither writable nor readable

    # Form for adding ponds
    form = SQLFORM(db.pond, _id="pond-form").process()
    # Create and process a form for adding a new pond entry

    # Fetch user's ponds
    pond_query = (db.pond.created_by == auth.user.id)
    # Query for ponds created by the logged-in user
    pond_fields = [db.pond.name]
    # Specify the fields to be shown in the pond list (just the name)
    response.js= ("alert('test');")
    # Pass selected pond ID via URL
    pond_links = [
        dict(header='', body=lambda row: A(row.name,
                                           #_href="#",**{'_data-pond-id': row.id},
                                           #_href=URL('default', 'get_rootstocks', args=[row.id]),
                                           _href=URL('default', 'get_rootstocks', vars={'pond_id': row.id}), 
                                           _class="pond-link"
                                           ))
    ]
    # Create links for each pond that will pass the pond ID in the URL when clicked
    response.js= ("alert('%s');" % row.id)
    # Grid for displaying ponds
    pond_grid = SQLFORM.grid(pond_query, fields=pond_fields, links=pond_links, create=False, editable=False, deletable=False,
                             details=False, paginate=10, csv=False, user_signature=False)
    # Display a grid of ponds filtered by the query and configured to not allow creating, editing, or deleting

    return dict(message=None, form=form, grid=pond_grid, rootstock_form=None, rootstock_grid=None, knotstock_list_grid=None)
    # Return the form for adding ponds, the grid displaying ponds, and other sections set to None (rootstock and knotstock are not yet loaded)

def get_rootstocks():
    """ Returns rootstocks belonging to the selected pond (AJAX call) """
    response.js= ("alert(%s);" % request.vars.pond_id)
    pond_id = request.vars.pond_id
    #pond_id = request.args(0, cast=int)
    # Retrieve the pond_id from the request URL parameters

    # Handle case where pond_id is null or invalid
    try:
        pond_id = int(pond_id)  # Convert to integer
    except (ValueError, TypeError):
        return DIV("Error: Invalid pond selected.")
    # Try to convert the pond_id to an integer. If it fails, return an error message

    query = (db.rootstock.pond == pond_id)
    # Query for rootstocks belonging to the selected pond
    fields = [db.rootstock.name]
    # Only show the 'name' field of the rootstock in the grid

    grid = SQLFORM.grid(query, fields=fields, create=False, editable=False, deletable=False,
                        details=False, paginate=10, csv=False, user_signature=False)
    # Display a grid of rootstocks for the selected pond, with pagination and other features disabled

    return grid
    # Return the grid for displaying rootstocks

def get_rootstock_form():
    """Returns the rootstock form for a selected pond (AJAX call)"""
    pond_id = request.vars.pond_id
    # Retrieve the pond_id from the request URL parameters

    if not pond_id:
        return DIV("Error: No pond selected.")
    # If pond_id is missing, return an error message

    try:
        pond_id = int(pond_id)  # Ensure pond_id is an integer
    except ValueError:
        return DIV("Error: Invalid pond ID.")
    # Try to convert pond_id to an integer. If it fails, return an error message

    # Create a form for adding rootstocks
    db.rootstock.pond.default = pond_id
    form = SQLFORM(db.rootstock)
    # Set the default pond for the rootstock form and generate the form

    return form
    # Return the form for adding a rootstock

def get_knotstock_list():
    """Returns items from knotstock_list associated with the selected rootstock (AJAX call)"""
    rootstock_id = request.vars.rootstock_id
    # Retrieve the rootstock_id from the request URL parameters

    if not rootstock_id:
        return DIV("Error: No rootstock selected.")
    # If rootstock_id is missing, return an error message

    try:
        rootstock_id = int(rootstock_id)  # Ensure rootstock_id is an integer
    except ValueError:
        return DIV("Error: Invalid rootstock ID.")
    # Try to convert rootstock_id to an integer. If it fails, return an error message

    query = (db.knotstock_list.rootstock == rootstock_id)
    fields = [db.knotstock_list.knotstock]
    # Query for knotstocks related to the selected rootstock, displaying their names

    grid = SQLFORM.grid(query, fields=fields, create=False, editable=False, deletable=False,
                        details=False, paginate=10, csv=False, user_signature=False)
    # Display a grid of knotstocks for the selected rootstock

    return grid
    # Return the grid for displaying knotstocks

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})
    # Provides an API endpoint to get the email of the logged-in user (only for GET requests)

# ---- Smart Grid (example) -----
@auth.requires_membership('admin')  # can only be accessed by members of admin group
def grid():
    response.view = 'generic.html'  # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    # Provide a smart grid for managing a table, based on a table name passed in the URL

    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu()  # add the wiki to the menu
    return auth.wiki()  # Return the wiki page

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    Exposes various authentication-related routes, like login, logout, register, profile, etc.
    """
    return dict(form=auth())  # Show the authentication forms for login, registration, etc.

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    Allows downloading of uploaded files.
    """
    return response.download(request, db)  # Handles file download requests from the server
