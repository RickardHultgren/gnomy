# -*- coding: utf-8 -*-

def index():
    if not auth.is_logged_in():
        return dict(message="please log in")

    # Pond form for creating new ponds
    pond_form = SQLFORM(db.pond).process()

    # Query user's ponds
    ponds = db(db.pond.created_by == auth.user_id).select()

    return dict(pond_form=pond_form, ponds=ponds)

##################

def get_rootstocks():
    """Fetches all rootstocks for the pond."""
    pond_id = request.vars.pond_id
    if not pond_id:
        return response.json({"error": "Missing pond_id"})

    rootstocks = db(db.rootstock.pond == pond_id).select(db.rootstock.id, db.rootstock.name)

    return response.json({"rootstocks": [{"id": r.id, "name": r.name} for r in rootstocks]})


def add_rootstock():
    """Handles adding a new rootstock to a pond via AJAX."""
    pond_id = request.vars.pond_id
    name = request.vars.name

    if not pond_id or not name:
        return "Invalid input"

    db.rootstock.insert(pond=pond_id, name=name, created_by=auth.user_id)
    return "Rootstock added successfully"
##################
def add_knotstock():
    """Handles adding a new knotstock relation via AJAX."""
    rootstock_id = request.vars.rootstock_id
    knotstock_id = request.vars.knotstock_id

    if not rootstock_id or not knotstock_id:
        return "Missing parameters."

    db.knotstock_list.insert(rootstock=rootstock_id, knotstock=knotstock_id, created_by=auth.user_id)
    return "Knotstock added successfully."

def get_knotstocks():
    """Fetches knotstocks for a given rootstock."""
    rootstock_id = request.vars.rootstock_id
    if not rootstock_id:
        return response.json({"error": "Missing rootstock_id"})

    knotstocks = db(db.knotstock_list.rootstock == rootstock_id).select(
        db.knotstock_list.knotstock, db.knotstock_list.created_by
    )

    # Convert results to JSON
    knotstock_data = [
        {"knotstock_name": row.knotstock.name, "created_by": row.created_by} for row in knotstocks
    ]

    return response.json({"knotstocks": knotstock_data})



def add_knotstock():
    """Handles adding a new knotstock relation via AJAX."""
    rootstock_id = request.vars.rootstock_id
    knotstock_id = request.vars.knotstock_id

    if not rootstock_id or not knotstock_id:
        return "Missing parameters."

    db.knotstock_list.insert(rootstock=rootstock_id, knotstock=knotstock_id, created_by=auth.user_id)
    return "Knotstock added successfully."
###############

















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
