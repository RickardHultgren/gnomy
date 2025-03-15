# -*- coding: utf-8 -*-

def index():
    if not auth.is_logged_in():
        return dict(message="please log in")

    # Pond form for creating new ponds
    pond_form = SQLFORM(db.pond).process()

    # Query user's ponds
    ponds = db(db.pond.created_by == auth.user_id).select()

    return dict(pond_form=pond_form, ponds=ponds)

############

def get_rootstocks():
    """Returns the rootstocks for a given pond ID (AJAX call)."""
    pond_id = request.vars.pond_id
    if not pond_id:
        return "Invalid pond ID"

    # Query rootstocks by pond
    rootstocks = db(db.rootstock.pond == pond_id).select()

    # Return a JSON response
    return response.json(dict(rootstocks=[rootstock.as_dict() for rootstock in rootstocks]))

def add_rootstock():
    """Handles adding a new rootstock to a pond via AJAX."""
    pond_id = request.vars.pond_id
    name = request.vars.name

    if not pond_id or not name:
        return "Invalid input"

    db.rootstock.insert(pond=pond_id, name=name, created_by=auth.user_id)
    return "Rootstock added successfully"

############

def get_knotstocks():
    """Returns the knottocks for a given rootstock ID (AJAX call)."""
    rootstock_id = request.vars.rootstock_id
    if not rootstock_id:
        return "Invalid rootstock ID"

    # Query rootstocks by pond
    knotstock_items = db(db.knotstock_list.rootstock == rootstock_id).select()

    # Return a JSON response
    return response.json(dict(knotstock_items=[knotstock_list.as_dict() for knotstock_item in knotstock_items]))

def add_knotstock():
    """Handles adding a new knotstock to a rootstock via AJAX."""
    rootstock_id = request.vars.rootstock_id
    knotstock_id = request.vars.knotstock_id

    if not rootstock_id or not knotstock_id:
        return response.json({"success": False, "error": "Missing rootstock or knotstock ID."})

    try:
        db.knotstock_list.insert(
            rootstock=rootstock_id,
            knotstock=knotstock_id,
            created_by=auth.user_id
        )
        return response.json({"success": True, "message": "Knotstock added successfully"})
    except Exception as e:
        return response.json({"success": False, "error": str(e)})

def get_knotstocks():
    """Returns a list of knotstocks for a given rootstock."""
    rootstock_id = request.vars.rootstock_id

    if not rootstock_id:
        return response.json({"success": False, "error": "Missing rootstock ID."})

    knotstocks = db(db.knotstock_list.rootstock == rootstock_id).select(
        db.knotstock_list.knotstock, db.knotstock_list.created_by
    )

    result = [
        {
            "knotstock_name": db.rootstock[k.knotstock].name if k.knotstock else "Unknown",
            "created_by": db.auth_user[k.created_by].first_name if k.created_by else "Unknown"
        }
        for k in knotstocks
    ]

    return response.json({"success": True, "knotstocks": result})

############

def get_flowers():
    """Fetches flowers linked to a rootstock via flower_list."""
    rootstock_id = request.vars.rootstock_id
    if not rootstock_id:
        return response.json({"error": "Missing rootstock_id"})

    flowers = db(
        (db.flower_list.rootstock == rootstock_id) & (db.flower_list.flower == db.flower.id)
    ).select(db.flower.id, db.flower.name, db.flower.flower_type, db.flower.growing_place)

    flower_data = [
        {"id": f.id, "name": f.name, "flower_type": f.flower_type, "growing_place": f.growing_place} 
        for f in flowers
    ]

    return response.json({"flowers": flower_data})


def add_flower():
    """Handles adding a new flower and linking it to a rootstock."""
    flower_name = request.vars.flower_name
    flower_type = request.vars.flower_type
    growing_place = request.vars.growing_place
    rootstock_id = request.vars.rootstock_id

    if not (flower_name and flower_type and growing_place and rootstock_id):
        return "Missing parameters."

    pond_id = db.rootstock(rootstock_id).pond if rootstock_id else None
    if not pond_id:
        return "Invalid rootstock."

    flower_id = db.flower.insert(
        name=flower_name, 
        pond=pond_id, 
        flower_type=flower_type, 
        growing_place=growing_place, 
        created_by=auth.user_id
    )

    db.flower_list.insert(rootstock=rootstock_id, flower=flower_id, created_by=auth.user_id)

    return "Flower added successfully."

#############



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
