:{{extend 'layout.html'}}

{{if message:}}
    <div>{{=message}}</div>
{{pass}}

{{if form:}}
    <h2>Add a New Pond</h2>
    {{=form}}
{{pass}}


<script>
function loadPond(pond_id) {
    $("#pond-container").load("{{=URL('pond')}}" + "/" + pond_id);
}
</script>

<div id="pond-container"></div>

<h2>Ponds</h2>
{{=grid}}













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
