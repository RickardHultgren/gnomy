# coding: utf-8

def index():
    """ Main page - shows login prompt or the user's ponds. """
    if not auth.user:
        return dict(message="Please log in", form=None, grid=None)

    # Define form for adding new ponds
    form = SQLFORM(db.pond)
    if form.process().accepted:
        response.flash = "Pond added!"
        redirect(URL('index'))  # Refresh grid after submission

    # Show only ponds owned by the logged-in user
    query = (db.pond.owner == auth.user.id)
    grid = SQLFORM.grid(
        query,
        create=False,
        editable=False,
        deletable=True,
        details=False,
        csv=False,
        links=[
            lambda row: A(row.name, _href="#", _onclick="loadPond({})".format(row.id))
        ]
    )

    return dict(message=None, form=form, grid=grid)


def pond():
    """ Load pond details and rootstock grid dynamically. """
    pond_id = request.args(0, cast=int)
    pond = db.pond(pond_id) or redirect(URL('index'))

    # Rootstock form, linked to the specific pond
    form = SQLFORM(db.rootstock)
    form.vars.pond = pond_id  # Pre-fill pond ID
    if form.process().accepted:
        response.flash = "Rootstock added!"
        redirect(URL('pond', args=[pond_id]))

    # Rootstock grid (filtered by pond)
    query = (db.rootstock.pond == pond_id)
    grid = SQLFORM.grid(
        query,
        create=False,
        editable=False,
        deletable=True,
        details=False,
        csv=False
    )

    return dict(pond=pond, form=form, grid=grid)









# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})
    # Provides an API endpoint to get the email of the logged-in user (only for GET requests)

# ---- Smart Grid (example) -----
@auth.requires_membership('admin')  # can only be accessed by members of admin group
def grid():
    response.view = 'generic.html'  # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    # Provide a smart grid for managing a table, based on a table name passed in the URL

    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu()  # add the wiki to the menu
    return auth.wiki()  # Return the wiki page

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    Exposes various authentication-related routes, like login, logout, register, profile, etc.
    """
    return dict(form=auth())  # Show the authentication forms for login, registration, etc.

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    Allows downloading of uploaded files.
    """
    return response.download(request, db)  # Handles file download requests from the server
