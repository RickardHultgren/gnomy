# -*- coding: utf-8 -*-

def index():
    if not auth.is_logged_in():
        return dict(message="Please log in")

    pond_form = SQLFORM(db.pond, _id="pondform").process()  # Add _id attribute
    ponds = db(db.pond.created_by == auth.user_id).select()
    session.pond_id = None
    session.rootstock_id = None
    return dict(pond_form=pond_form, ponds=ponds)

@auth.requires_login()  # or remove if public access is okay
def set_rootstockid():
    rootstock_id = request.vars.rootstock_id
    if rootstock_id:
        session.rootstock_id = rootstock_id
        return response.json({'status': 'success', 'message': 'Rootstock ID saved.'})
    else:
        return response.json({'status': 'error', 'message': 'No rootstock ID provided'})


def get_rootstocks():
    pond_id = request.vars.pond_id
    session.pond_id = pond_id
    if not pond_id:
        return response.json({"status": "error", "error": "No pond ID provided"})

    try:
        pond_id = int(pond_id)
    except ValueError:
        return response.json({"status": "error", "error": "Invalid pond ID"})

    rootstocks = db(db.rootstock.pond == pond_id).select()
    
    multipleTendrils = []
    multipleFlowers = []

    for rootstock in rootstocks:
        tendrils = db(db.tendril.rootstock == rootstock.id).select()
        flowers = db(db.flower.rootstock == rootstock.id).select()

        multipleTendrils.extend([
            {
                "rootstock_id": rootstock.id,
                "knotstock_id": t.knotstock,
                "id": t.id,
                "name": t.name,
                "carry": t.get("carry"),
                "suffuse": t.get("suffuse")
            } for t in tendrils
        ])

        multipleFlowers.extend([
            {
                "rootstock_id": rootstock.id,
                "id": f.id,
                "name": f.name,
                "fragrance": f.get("fragrance"),
                "fruit": f.get("fruit")
            } for f in flowers
        ])

    return response.json({
        "status": "success",
        "pond_id": pond_id,
        "rootstocks": [r.as_dict() for r in rootstocks],
        "multipleTendrils": multipleTendrils,
        "multipleFlowers": multipleFlowers
    })


    
    return response.json(dict(rootstocks=[r.as_dict() for r in rootstocks]))


def add_rootstock():
    pond_id = request.vars.pond_id
    name = request.vars.name
    rootstock = db.rootstock.insert(pond=pond_id, name=name, created_by=auth.user_id)
    session.rootstock_id = rootstock.id  # Store the new rootstock ID in the session

    return response.json({"status": "success", "rootstock_id": rootstock.id})





def delete_rootstock():
    try:
        rootstock_id = int(request.vars.rootstock_id or 0)
    except ValueError:
        return response.json({"status": "error", "message": "Invalid rootstock ID"})

    rootstock = db.rootstock(rootstock_id)
    if not rootstock:
        return response.json({"status": "error", "message": "Rootstock not found"})

    if rootstock.created_by != auth.user_id:
        return response.json({"status": "error", "message": "Not authorized to delete this rootstock"})

    db(db.rootstock.id == rootstock_id).delete()
    return response.json({"status": "success", "message": "Rootstock deleted"})

#def rootstock_tool():
#    session.rootstock_id = request.vars.rootstock_id
#    return "OK"


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

    return response.json({
        "status": "success",
        "tendrils": [
            {   
                #"rootstock_id": rootstock_id,
                "id": t.id,
                "name": t.name,
                "carry": t.carry if "carry" in t else None,
                "suffuse": t.suffuse if "suffuse" in t else None
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
        return response.json({"status": "error", "error": "Missing required fields (rootstock_id)"})

    # Ensure the user is logged in
    if not auth.user_id:
        return response.json({"status": "error", "error": "User not authenticated"})

    # Convert rootstock_id to an integer
    try:
        rootstock_id = int(rootstock_id)
    except ValueError:
        return response.json({"status": "error", "error": "Invalid rootstock ID"})

    tendril_id = db.tendril.insert(
        rootstock=rootstock_id,
        knotstock=knotstock_id if knotstock_id else None,  # Allow nullable values
        name=tendril_name,
        carry=tendril_carry,
        suffuse=tendril_suffuse,
        created_by=auth.user_id
    )

    return response.json({"status": "success", "tendril_id": tendril_id})

def get_flowers():
    rootstock_id = request.vars.rootstock_id
    
    if not rootstock_id or not rootstock_id.isdigit():
        return response.json({"status": "error", "error": "Invalid or missing rootstock ID"})

    flowers = db(db.flower.rootstock == int(rootstock_id)).select()

    return response.json({
        "status": "success",
        "flowers": [
            {   
                #"rootstock_id": rootstock_id,
                "id": t.id,
                "name": t.name,
                "fruit": t.fruit if "fruit" in t else None,
                "fragrance": t.fragrance if "fragrance" in t else None
            } for t in flowers
        ]
    })


def add_flower():
    rootstock_id = session.rootstock_id

    if rootstock_id is None:
        return response.json({"status": "error", "error": "Rootstock ID is missing in session"})

    flower_name = request.post_vars.flower_name
    flower_fruit = request.post_vars.flower_fruit
    flower_fragrance = request.post_vars.flower_fragrance

    if not flower_name:
        return response.json({"status": "error", "error": "Flower name is required"})

    # Ensure the user is logged in
    if not auth.user_id:
        return response.json({"status": "error", "error": "User not authenticated"})

    # Convert rootstock_id to an integer
    try:
        rootstock_id = int(rootstock_id)
    except ValueError:
        return response.json({"status": "error", "error": "Invalid rootstock ID"})

    flower_id = db.flower.insert(
        rootstock=rootstock_id,
        name=flower_name,
        fruit=flower_fruit,
        fragrance=flower_fragrance,
        created_by=auth.user_id
    )

    return response.json({"status": "success", "flower_id": flower_id})












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