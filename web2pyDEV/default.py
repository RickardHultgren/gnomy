# -*- coding: utf-8 -*- 
from gluon import SQLFORM, URL, DIV, A, H2
from gluon.tools import Auth

# Initialize authentication system
auth = Auth(db)
auth.define_tables(username=False, signature=False)

def index():
    """ Home page: Displays ponds and rootstocks owned by the logged-in user. """
    if not auth.user:
        return dict(
            message="Please log in",
            pond_form=None,
            pond_grid=None,
            rootstock_form=None,
            rootstock_grid=None,
            knotstock_list_grid=None
        )

    # ---- Ponds Section ----
    db.pond.created_by.default = auth.user.id
    db.pond.created_by.writable = False
    db.pond.created_by.readable = False

    # Form for adding ponds
    pond_form = SQLFORM(db.pond, _id="pond-form").process()

    # Query for user's ponds
    user_ponds_query = (db.pond.created_by == auth.user.id)
    pond_display_fields = [db.pond.name]

    # Create links for each pond that will pass the pond ID in the URL when clicked
    pond_link_column = [
        dict(
            header='',
            body=lambda row: A(
                row.name,
                _href=URL('default', 'get_rootstocks', vars={'pond_id': row.id}),
                _class="pond-link"
            )
        )
    ]

    # Grid for displaying ponds
    pond_grid = SQLFORM.grid(
        user_ponds_query,
        fields=pond_display_fields,
        links=pond_link_column,
        create=False, editable=False, deletable=False,
        details=False, paginate=10, csv=False, user_signature=False
    )

    return dict(
        message=None,
        pond_form=pond_form,
        pond_grid=pond_grid,
        rootstock_form=None,
        rootstock_grid=None,
        knotstock_list_grid=None
    )

def get_rootstocks():
    """ Returns rootstocks belonging to the selected pond (AJAX call) """
    pond_id = request.vars.pond_id

    if not pond_id:
        return DIV("Error: No pond selected.")

    try:
        pond_id = int(pond_id)  
    except ValueError:
        return DIV("Error: Invalid pond ID.")

    # Query for rootstocks belonging to the selected pond
    rootstock_query = (db.rootstock.pond == pond_id)
    rootstock_display_fields = [db.rootstock.name]

    rootstock_grid = SQLFORM.grid(
        rootstock_query,
        fields=rootstock_display_fields,
        create=False, editable=False, deletable=False,
        details=False, paginate=10, csv=False, user_signature=False
    )

    return dict(pond_id=pond_id, rootstock_grid=rootstock_grid)

def get_rootstock_form():
    """Returns the rootstock form for a selected pond (AJAX call)"""
    pond_id = request.vars.pond_id

    if not pond_id:
        return DIV("Error: No pond selected.")

    try:
        pond_id = int(pond_id)
    except ValueError:
        return DIV("Error: Invalid pond ID.")

    # Create a form for adding rootstocks
    db.rootstock.pond.default = pond_id
    rootstock_form = SQLFORM(db.rootstock)

    return rootstock_form

def get_knotstock_list():
    """Returns items from knotstock_list associated with the selected rootstock (AJAX call)"""
    rootstock_id = request.vars.rootstock_id

    if not rootstock_id:
        return DIV("Error: No rootstock selected.")

    try:
        rootstock_id = int(rootstock_id)  
    except ValueError:
        return DIV("Error: Invalid rootstock ID.")

    knotstock_query = (db.knotstock_list.rootstock == rootstock_id)
    knotstock_display_fields = [db.knotstock_list.knotstock]

    knotstock_grid = SQLFORM.grid(
        knotstock_query,
        fields=knotstock_display_fields,
        create=False, editable=False, deletable=False,
        details=False, paginate=10, csv=False, user_signature=False
    )

    return knotstock_grid

# ---- API Example -----
@auth.requires_login()
def api_get_user_email():
    """API endpoint to get the email of the logged-in user"""
    if not request.env.request_method == 'GET': 
        raise HTTP(403)
    return response.json({'status': 'success', 'email': auth.user.email})

# ---- Smart Grid ----
@auth.requires_membership('admin')
def grid():
    """Smart grid for managing a table, restricted to admins"""
    response.view = 'generic.html'
    table_name = request.args(0)
    if not table_name in db.tables:
        raise HTTP(403)
    
    admin_grid = SQLFORM.smartgrid(
        db[table_name], 
        args=[table_name], 
        deletable=False, editable=False
    )

    return dict(grid=admin_grid)

# ---- Embedded wiki ----
def wiki():
    """Returns the wiki page"""
    auth.wikimenu()  
    return auth.wiki()  

# ---- User authentication routes ----
def user():
    """Handles login, logout, registration, profile, etc."""
    return dict(form=auth())

# ---- File download handling ----
@cache.action()
def download():
    """Handles file downloads"""
    return response.download(request, db)
