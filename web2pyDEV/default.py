# -*- coding: utf-8 -*-
from gluon import current

def index():
    """
    If the user is not logged in, display a message prompting them to log in.
    If logged in, display a grid of ponds owned by the user and handle pond creation.
    """
    auth = current.auth
    db = current.db
    response = current.response

    if not auth.user:
        # User is not logged in
        return dict(message="Please log in", grid=None, pond_form=None, rootstock_grids={})

    # User is logged in
    user_id = auth.user.id

    # Define the pond form
    pond_form = SQLFORM(db.pond)
    if pond_form.process().accepted:
        response.flash = 'New pond added'
    elif pond_form.errors:
        response.flash = 'Form has errors'

    # Display ponds owned by the user
    ponds = db(db.pond.owner == user_id).select()

    # Generate grids for each pond's rootstocks
    rootstock_grids = {}
    for pond in ponds:
        query = (db.rootstock.pond == pond.id)
        rootstock_grids[pond.id] = SQLFORM.grid(query, user_signature=False, create=True)

    return dict(message=None, grid=ponds, pond_form=pond_form, rootstock_grids=rootstock_grids)


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
