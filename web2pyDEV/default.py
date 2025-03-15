# -*- coding: utf-8 -*-

def index():
    if not auth.is_logged_in():
        return dict(message="please log in")

    pond_form = SQLFORM(db.pond).process()
    ponds = db(db.pond.created_by == auth.user_id).select()

    return dict(pond_form=pond_form, ponds=ponds)

def get_rootstocks():
    pond_id = request.vars.pond_id
    rootstocks = db(db.rootstock.pond == pond_id).select()
    return response.json(dict(rootstocks=[r.as_dict() for r in rootstocks]))

def add_rootstock():
    pond_id = request.vars.pond_id
    name = request.vars.name
    db.rootstock.insert(pond=pond_id, name=name, created_by=auth.user_id)
    return "Rootstock added successfully"

def get_knotstocks():
    rootstock_id = request.vars.rootstock_id
    knotstocks = db(db.knotstock_list.rootstock == rootstock_id).select(db.knotstock_list.knotstock)
    
    result = []
    for knot in knotstocks:
        knotstock = db.rootstock(knot.knotstock)
        if knotstock:
            result.append({"knotstock_name": knotstock.name})

    return response.json(dict(knotstocks=result))

    
def add_knotstock():
    rootstock_id = request.vars.rootstock_id
    knotstock_id = request.vars.knotstock_id
    db.knotstock_list.insert(rootstock=rootstock_id, knotstock=knotstock_id, created_by=auth.user_id)
    return "Knotstock added successfully"

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

def get_tendrils():
    rootstock_id = request.vars.rootstock_id
    tendrils = db(db.tendril.rootstock == rootstock_id).select()

    result = []
    for tendril in tendrils:
        knotstock = db.rootstock(tendril.knotstock)
        if knotstock:
            result.append({"tendril_name": tendril.name, "knotstock_name": knotstock.name})

    return response.json(dict(tendrils=result))

def add_tendril():
    rootstock_id = request.vars.rootstock_id
    knotstock_id = request.vars.knotstock_id
    tendril_name = request.vars.tendril_name  # Added for the tendril name field

    db.tendril.insert(rootstock=rootstock_id, knotstock=knotstock_id, name=tendril_name, created_by=auth.user_id)
    return "Tendril added successfully"










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
