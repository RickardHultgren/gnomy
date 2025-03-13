# -*- coding: utf-8 -*-
from gluon import SQLFORM, URL, DIV, A, H2, H3  # Import necessary web2py modules for form creation and UI elements
from gluon.tools import Auth  # Import authentication system

# Initialize authentication system
auth = Auth(db)
auth.define_tables(username=False, signature=False)  # Define user authentication tables

def index():
    """ Home page: Displays ponds owned by the logged-in user. Allows users to add new ponds. """
    if not auth.user:  # Check if the user is logged in
        message = "Please log in"  # Show a message if not logged in
        return dict(message=message, form=None, grid=None)  # Return message without form and grid
    else:
        db.pond.created_by.default = auth.user.id  # Set the default owner of a new pond to the logged-in user
        db.pond.created_by.writable = False  # Prevent the user from modifying the owner field
        db.pond.created_by.readable = False  # Hide the owner field in forms

        # Create a form for adding new ponds
        form = SQLFORM(db.pond).process()

        # Query to fetch ponds owned by the logged-in user
        query = (db.pond.created_by == auth.user.id)
        fields = [db.pond.name]  # Only display the pond's name
        links = [
            dict(header='', body=lambda row: A(row.name, _href='#', _onclick="loadPond(%d)" % row.id))  # Clickable pond names
        ]
        # Generate a grid to display the user's ponds
        grid = SQLFORM.grid(query, fields=fields, links=links, create=False, editable=False, deletable=False, details=False, paginate=10, csv=False, user_signature=False)

        return dict(message=None, form=form, grid=grid)  # Return the form and grid for rendering

def pond():
    """ Displays a selected pond along with a form and grid for its rootstocks. """
    pond_id = request.args(0, cast=int)  # Get the pond ID from the URL
    pond = db.pond(pond_id) or redirect(URL('index'))  # Fetch the pond or redirect if not found

    # Set up a form to add a new rootstock linked to this pond
    db.rootstock.pond_id.default = pond.id  # Assign this pond's ID to the new rootstock
    db.rootstock.pond_id.writable = False  # Prevent users from modifying the pond_id field
    db.rootstock.pond_id.readable = False  # Hide the pond_id field in forms
    db.rootstock.created_by.default = auth.user.id  # Set the creator to the logged-in user
    db.rootstock.created_by.writable = False  # Prevent users from modifying the creator field
    db.rootstock.created_by.readable = False  # Hide the creator field in forms

    # Create the form for adding a new rootstock (only if the user is logged in)
    form = SQLFORM(db.rootstock).process() if auth.user else None

    # Query to fetch all rootstocks belonging to the selected pond
    query = (db.rootstock.pond_id == pond.id)
    fields = [db.rootstock.name]  # Only display the rootstock's name
    links = [
        dict(header='', body=lambda row: A(row.name, _href='#', _onclick="loadRootstock(%d)" % row.id))  # Clickable rootstock names
    ]
    # Generate a grid to display rootstocks belonging to this pond
    grid = SQLFORM.grid(query, fields=fields, links=links, create=False, editable=False, deletable=False, details=False, paginate=10, csv=False, user_signature=False)

    return dict(pond=pond, form=form, grid=grid)  # Return pond details, form, and grid

def rootstock():
    """ Displays the selected rootstock's name. """
    rootstock_id = request.args(0, cast=int)  # Get the rootstock ID from the URL
    rootstock = db.rootstock(rootstock_id) or redirect(URL('index'))  # Fetch the rootstock or redirect if not found
    return DIV(H3(rootstock.name))  # Return a div displaying the rootstock's name
