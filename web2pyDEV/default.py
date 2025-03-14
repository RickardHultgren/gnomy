# -*- coding: utf-8 -*-
from gluon import SQLFORM, URL, DIV, A, H2, H3  # Import necessary web2py modules for form creation and UI elements
from gluon.tools import Auth  # Import authentication system

db = DAL('sqlite://storage.sqlite')  # or your database connection
auth = Auth(db)
auth.define_tables(username=False, signature=False)


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
