# -*- coding: utf-8 -*-
from gluon import SQLFORM, URL, DIV, A, H2
from gluon.tools import Auth

# Initialize authentication system
auth = Auth(db)
auth.define_tables(username=False, signature=False)

def index():
    """ Home page: Displays ponds and rootstocks owned by the logged-in user. """
    if not auth.user:
        return dict(message="Please log in", form=None, grid=None, rootstock_form=None, rootstock_grid=None)

    # ---- Ponds Section ----
    db.pond.created_by.default = auth.user.id
    db.pond.created_by.writable = False
    db.pond.created_by.readable = False

    # Form for adding ponds
    form = SQLFORM(db.pond, _id="pond-form").process()

    # Fetch user's ponds
    pond_query = (db.pond.created_by == auth.user.id)
    pond_fields = [db.pond.name]

    # Pass selected pond ID via URL
    pond_links = [
        dict(header='', body=lambda row: A(row.name, 
                                           _href="#", 
                                           _class="pond-link", 
                                           _data_pond_id=row.id))
    ]

    # Grid for displaying ponds
    pond_grid = SQLFORM.grid(pond_query, fields=pond_fields, links=pond_links, create=False, editable=False, deletable=False,
                             details=False, paginate=10, csv=False, user_signature=False)

    return dict(message=None, form=form, grid=pond_grid, rootstock_form=None, rootstock_grid=None)

def get_rootstocks():
    """ Returns rootstocks belonging to the selected pond (AJAX call) """
    pond_id = request.vars.pond_id

    # Handle case where pond_id is null or invalid
    try:
        pond_id = int(pond_id)  # Convert to integer
    except (ValueError, TypeError):
        return DIV("Error: Invalid pond selected.")

    query = (db.rootstock.pond == pond_id)
    fields = [db.rootstock.name]

    grid = SQLFORM.grid(query, fields=fields, create=False, editable=False, deletable=False,
                        details=False, paginate=10, csv=False, user_signature=False)

    return grid

def get_rootstocks():
    """ Returns rootstocks belonging to the selected pond (AJAX call) """
    pond_id = request.vars.pond_id

    if not pond_id:
        return DIV("No pond selected.")

    query = (db.rootstock.pond == pond_id)
    fields = [db.rootstock.name]

    # Fix: Removed invalid `_id` argument
    grid = SQLFORM.grid(query, fields=fields, create=False, editable=False, deletable=False,
                        details=False, paginate=10, csv=False, user_signature=False)

    return grid

def get_rootstocks():
    """ Returns rootstocks belonging to the selected pond (AJAX call) """
    pond_id = request.vars.pond_id

    # Handle case where pond_id is null or invalid
    try:
        pond_id = int(pond_id)  # Convert to integer
    except (ValueError, TypeError):
        return DIV("Error: Invalid pond selected.")

    query = (db.rootstock.pond == pond_id)
    fields = [db.rootstock.name]

    grid = SQLFORM.grid(query, fields=fields, create=False, editable=False, deletable=False,
                        details=False, paginate=10, csv=False, user_signature=False)

    return grid






# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki()

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
