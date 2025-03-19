# -*- coding: utf-8 -*-

def index():
    if not auth.is_logged_in():
        return dict(message="please log in")

    pond_form = SQLFORM(db.pond).process()
    ponds = db(db.pond.created_by == auth.user_id).select()
    session.pond_id = None
    session.rootstock_id = None
    return dict(pond_form=pond_form, ponds=ponds)

def get_rootstocks():
    pond_id = request.vars.pond_id
    if not pond_id:
        return response.json({"error": "No pond ID provided"})

    rootstocks = db(db.rootstock.pond == pond_id).select()
    return response.json(dict(rootstocks=[r.as_dict() for r in rootstocks]))


def add_rootstock():
    pond_id = request.vars.pond_id
    name = request.vars.name
    rootstock = db.rootstock.insert(pond=pond_id, name=name, created_by=auth.user_id)
    session.rootstock_id = rootstock.id  # Store the new rootstock ID in the session

    return response.json({"status": "success", "rootstock_id": rootstock.id})

def set_rootstock_id():
    rootstock_id = request.post_vars.get('rootstock_id')

    if not rootstock_id or not rootstock_id.isdigit():
        return response.json({"error": "Invalid rootstock ID"})

    rootstock = db.rootstock(int(rootstock_id))

    if not rootstock:
        return response.json({"error": "Rootstock not found"})

    session.rootstock_id = rootstock.id  # Store valid ID only

    return response.json({
        "status": "success",
        "rootstock_id": rootstock_id,
        "rootstock_name": rootstock.name
    })
    
def get_tendrils():
    rootstock_id = request.vars.rootstock_id

    if not rootstock_id or not rootstock_id.isdigit():
        return response.json({"status": "error", "error": "Invalid or missing rootstock ID"})

    tendrils = db(db.tendril.rootstock == int(rootstock_id)).select()

    # Ensure the fields exist before accessing them
    field_names = db.tendril.fields

    return response.json({
        "status": "success",
        "tendrils": [
            {
                "id": t.id,
                "name": t.name,
                "carry": t.carry if "carry" in field_names else None,
                "suffuse": t.suffuse if "suffuse" in field_names else None
            } for t in tendrils
        ]
    })



def add_tendril():
    rootstock_id = session.rootstock_id
    knotstock_id = request.post_vars.knotstock_id
    tendril_name = request.post_vars.tendril_name
    tendril_carry = request.post_vars.tendril_carry
    tendril_suffuse = request.post_vars.tendril_suffuse

    if not rootstock_id or not tendril_name:
        return response.json({"status": "error", "error": "Missing required fields"})

    # Ensure the user is logged in
    if not auth.user_id:
        return response.json({"status": "error", "error": "User not authenticated"})

    # Convert rootstock_id to an integer
    try:
        rootstock_id = int(rootstock_id)
    except ValueError:
        return response.json({"status": "error", "error": "Invalid rootstock ID"})

    tendril_id = db.tendril.insert(
        rootstock=session.rootstock_id,
        knotstock=knotstock_id if knotstock_id else None,  # Allow nullable values
        name=tendril_name,
        carry=tendril_carry,
        suffuse=tendril_suffuse,
        created_by=auth.user_id
    )

    return response.json({"status": "success", "tendril_id": tendril_id})

def get_flowers():
    rootstock_id = request.vars.rootstock_id
    flowers = db(db.flower_list.rootstock == rootstock_id).select(db.flower.name)
    return response.json(dict(flowers=[{"name": f.name} for f in flowers]))

def add_flower():
    rootstock_id = request.vars.rootstock_id
    name = request.vars.name

    flower_id = db.flower.insert(name=name, pond=session.pond_id, created_by=auth.user_id)
    db.flower_list.insert(rootstock=rootstock_id, flower=flower_id)

    return "Flower added successfully"











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
