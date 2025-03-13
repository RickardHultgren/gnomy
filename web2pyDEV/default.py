# -*- coding: utf-8 -*-
from gluon import SQLFORM, URL, DIV, A, H2, H3
from gluon.tools import Auth

# Initialize authentication system
auth = Auth(db)
auth.define_tables(username=False, signature=False)

def index():
    """ Home page: Displays ponds owned by the logged-in user. Allows users to add new ponds. """
    if not auth.user:
        return dict(message="Please log in", form=None, grid=None, pond_container=None, rootstock_container=None)

    db.pond.created_by.default = auth.user.id
    db.pond.created_by.writable = False
    db.pond.created_by.readable = False

    # Form for adding ponds
    form = SQLFORM(db.pond).process()

    # Fetch user's ponds
    query = (db.pond.created_by == auth.user.id)
    fields = [db.pond.name]
    links = [
        dict(header='', body=lambda row: A(row.name, _href='#', _class="pond-link", **{"data-pond-id": row.id}))
    ]

    # Display grid of ponds
    grid = SQLFORM.grid(query, fields=fields, links=links, create=False, editable=False, deletable=False,
                        details=False, paginate=10, csv=False, user_signature=False)

    return dict(message=None, form=form, grid=grid, pond_container=DIV(), rootstock_container=DIV())

def pond():
    """ Displays a pond with its rootstocks and form for adding new rootstocks. """
    pond_id = request.args(0, cast=int)
    pond = db.pond(pond_id) or redirect(URL('index'))

    # Set up rootstock form
    db.rootstock.pond_id.default = pond.id
    db.rootstock.pond_id.writable = False
    db.rootstock.pond_id.readable = False
    db.rootstock.created_by.default = auth.user.id
    db.rootstock.created_by.writable = False
    db.rootstock.created_by.readable = False

    form = SQLFORM(db.rootstock).process() if auth.user else None

    # Fetch rootstocks belonging to the pond
    query = (db.rootstock.pond_id == pond.id)
    fields = [db.rootstock.name]
    links = [
        dict(header='', body=lambda row: A(row.name, _href='#', _onclick="loadRootstock(%d);" % row.id))
    ]

    grid = SQLFORM.grid(query, fields=fields, links=links, create=False, editable=False, deletable=False,
                        details=False, paginate=10, csv=False, user_signature=False)

    return dict(pond=pond, form=form, grid=grid)

def rootstock():
    """ Displays a selected rootstock's details. """
    rootstock_id = request.args(0, cast=int)
    rootstock = db.rootstock(rootstock_id) or redirect(URL('index'))

    return dict(rootstock=rootstock)



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
