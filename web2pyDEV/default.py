# -*- coding: utf-8 -*-

def index():
    if not auth.is_logged_in():
        return dict(message="please log in")

    # Pond form for creating new ponds
    pond_form = SQLFORM(db.pond).process()

    # Query user's ponds
    ponds = db(db.pond.created_by == auth.user_id).select()

    return dict(pond_form=pond_form, ponds=ponds)

def get_ponds():
    """Fetch all ponds."""
    ponds = db(db.pond).select(db.pond.id, db.pond.name)
    return response.json({"ponds": [{"id": p.id, "name": p.name} for p in ponds]})


############

def get_rootstocks():
    """Fetch rootstocks for a selected pond."""
    pond_id = request.vars.pond_id
    if not pond_id:
        return response.json({"error": "Missing pond_id"})

    rootstocks = db(db.rootstock.pond == pond_id).select(db.rootstock.id, db.rootstock.name)
    return response.json({"rootstocks": [{"id": r.id, "name": r.name} for r in rootstocks]})

def add_rootstock():
    """Handles adding a new rootstock to a pond."""
    pond_id = request.vars.pond_id
    rootstock_name = request.vars.rootstock_name

    if not pond_id or not rootstock_name:
        return "Missing parameters."

    db.rootstock.insert(name=rootstock_name, pond=pond_id, created_by=auth.user_id)
    return "Rootstock added successfully."

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
    """Fetches flowers for a given rootstock."""
    rootstock_id = request.vars.rootstock_id
    if not rootstock_id:
        return response.json({"error": "Missing rootstock_id"})

    flower_list = db(db.flower_list.rootstock == rootstock_id).select(
        db.flower_list.flower
    )

    flowers = []
    for flower_entry in flower_list:
        flower = db(db.flower.id == flower_entry.flower).select().first()
        if flower:
            flowers.append({"name": flower.name, "flower_type": flower.flower_type})

    return response.json({"flowers": flowers})


def add_flower():
    """Handles adding a new flower and linking it to the selected rootstock."""
    name = request.vars.name
    flower_type = request.vars.flower_type
    growing_place = request.vars.growing_place
    rootstock_id = request.vars.rootstock_id

    if not name or not flower_type or not growing_place or not rootstock_id:
        return "Missing parameters."

    flower_id = db.flower.insert(
        name=name,
        pond=session.pond_id,
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
