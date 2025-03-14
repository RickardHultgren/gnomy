# -*- coding: utf-8 -*-
from gluon import SQLFORM, URL, DIV, A, H2
from gluon.tools import Auth

# Initialize authentication system
auth = Auth(db)
auth.define_tables(username=False, signature=False)

def index():
    """ 
    Home page: Displays ponds and rootstocks owned by the logged-in user.
    Allows users to add new ponds and rootstocks.
    """
    if not auth.user:
        return dict(message="Please log in", form=None, grid=None, rootstock_form=None, rootstock_grid=None, pond_container=None, rootstock_container=None)

    # ---- Ponds Section ----
    db.pond.created_by.default = auth.user.id
    db.pond.created_by.writable = False
    db.pond.created_by.readable = False

    # Form for adding ponds
    form = SQLFORM(db.pond).process()

    # Fetch user's ponds
    pond_query = (db.pond.created_by == auth.user.id)
    pond_fields = [db.pond.name]

    # Pass selected pond ID via URL
    pond_links = [
        dict(header='', body=lambda row: A(row.name, 
                                           _href=URL('default', 'index', vars={'selected_pond_id': row.id}), 
                                           _class="pond-link"))
    ]

    # Grid for displaying ponds
    pond_grid = SQLFORM.grid(pond_query, fields=pond_fields, links=pond_links, create=False, editable=False, deletable=False,
                             details=False, paginate=10, csv=False, user_signature=False)

    # ---- Rootstocks Section ----
    selected_pond_id = request.vars.selected_pond_id

    # If a pond is selected, set up the rootstock form for that pond
    if selected_pond_id:
        selected_pond = db.pond(selected_pond_id) or redirect(URL('index'))

        db.rootstock.pond.default = selected_pond.id
        db.rootstock.pond.writable = False  # Hide pond field in form
        db.rootstock.pond.readable = False
        db.rootstock.created_by.default = auth.user.id
        db.rootstock.created_by.writable = False
        db.rootstock.created_by.readable = False

        rootstock_form = SQLFORM(db.rootstock).process()
        rootstock_query = (db.rootstock.pond == selected_pond_id)
    else:
        rootstock_form = None  # No form shown if no pond selected
        rootstock_query = (db.rootstock.id == None)  # No rootstocks displayed

    rootstock_fields = [db.rootstock.name]
    rootstock_links = [
        dict(header='', body=lambda row: A(row.name, _href=URL('default', 'rootstock', args=[row.id]), _class="rootstock-link"))
    ]

    # Grid for displaying rootstocks
    rootstock_grid = SQLFORM.grid(rootstock_query, fields=rootstock_fields, links=rootstock_links, create=False, editable=False, deletable=False,
                                  details=False, paginate=10, csv=False, user_signature=False)

    return dict(message=None, form=form, grid=pond_grid, rootstock_form=rootstock_form, rootstock_grid=rootstock_grid, 
                pond_container=DIV(), rootstock_container=DIV())






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
