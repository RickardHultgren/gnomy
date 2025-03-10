from gluon.http import redirect
import json

session.the_id = int()
if not session.pond_id:
    session.pond_id = int(0)


if not session.rootstock_id:
    session.rootstock_id = int(0)

if not session.rootstocks_pass:
    session.rootstocks_pass = dict()

if not session.len_rootstocks_pass :
    session.len_rootstocks_pass

if not session.new_graph :
    session.new_graph = 0

def index():
    return locals()




def add_pond():
    # Check if the user is logged in
    if not auth.is_logged_in():
        redirect(URL('default', 'user', args='login'))

    # Process the form submission
    if request.method == 'POST':
        # Insert data into the 'pond' table based on form input
        inserted_id = db.pond.insert(**request.post_vars)

        response.flash = f'pond added successfully with ID: {inserted_id}'
        redirect(URL('default', 'index'))

    # Create an empty form
    form = SQLFORM(db.pond)

    response.js="document.getElementById('pondchoice').reload(true);"
    return dict()



def check():#(name):
    import gluon.contenttype
    id_list = request.args
    response.headers['Content-Type']=gluon.contenttype.contenttype('.js')
    #return ('alert("%s");'% id_list)


def addnext():
    # Ensure user is authenticated
    if not auth.user:
        raise HTTP(403, "Authentication required")

    # Extract data from the AJAX request
    nextname = request.vars.nextname

    # Ensure session.rootstock_id is set and valid
    if 'rootstock_id' not in session or not session.rootstock_id:
        raise HTTP(400, "Invalid session rootstock_id")

    # Retrieve the name of the current rootstock (assuming 'rootstock' table and 'name' field)
    current_rootstock = db.rootstock[session.rootstock_id]
    if not current_rootstock:
        raise HTTP(400, "rootstock not found in the database")

    name = current_rootstock.name

    # Insert a new record into the 'knotstock_list' table
    knotstock_id = db.knotstock_list.insert(
        name=name,
        nextname=nextname,
        created_by=auth.user.id,
    )

    # Reload the 'rootstockpond' element after successful insertion
    response.js = "document.getElementById('rootstockpond').reload(true);"
    response.js = "document.getElementById('foundcoll').reload(true);"

    # Return a JSON response indicating success and the ID of the inserted record
    return response.json(dict(success=True, id=nextrootstock_id))


def rootstockdelete():
    record_id = session.rootstock_id
    db(db.rootstock.id == record_id).delete()

    #response.js = "document.getElementById('rootstockpond').reload(true);"
    response.js = "document.getElementById('rootstockpond').reload(true);"
    response.js = "document.getElementById('foundcoll').reload(true);"
    return #"Record deleted successfully"

def rootstock_next_delete():
    record_id = request.vars.record_id
    # Perform delete operations on multiple tables
    knotstocks_delete = db(db.knotstock_list.rootstock==session.record_id)
    #db.table1(db.table1.id == record_id).delete()
    #db.table2(db.table2.id == record_id).delete()
    for next_del in knotstocks_delete:

        db.knotstock_list(db.knotstock_list.id == next_del.id).delete()
    db.rootstock(db.rootstock.id == record_id.id).delete()

    # Add more delete operations for other tables if needed

def shownextrootstocks():
    # Create a grid control.
    try:
        flowers_to_show = (db.flower_list.rootstock == session.rootstock_id)
    except:
        flowers_to_show = None  # Handle the case when session.rootstock_id is not set
    try:
        knotstocks_to_show = (db.knotstock_list.rootstock == session.rootstock_id)
    except:
        knotstocks_to_show = None  # Handle the case when session.rootstock_id is not set


    # Define function to check if a record can be edited by the current user
    def can_edit_record(row):
        if auth.is_logged_in():
            return row.created_by == auth.user.id
        return False

    # Define function to create a delete link for a rootstock record
    def can_delete_rootstock(row):
        if auth.is_logged_in() and row.created_by == auth.user.id:
            delete_url = URL('default', 'rootstock_delete', args=[row.id])
            return A('Delete!', 
                    _style="height:1em;", 
                    _href=delete_url, 
                    _class='btn btn-danger delete-btn',  # Use class instead
                    _data=dict(rootstock_id=row.id))  # Store ID in data attribute
        return None

    # Display the grid based on user authentication status
    if auth.is_logged_in():
        flower_grid = SQLFORM.grid(
            flowers_to_show,
            deletable=can_edit_record,
            fields=["knotstock"],
            #editable=can_edit_record,
            details=False,
            create=False,
            searchable=False,
            paginate=10,
            csv=False,
            sortable=False
        )
    else:
        flower_grid = SQLFORM.grid(
            flowers_to_show,
            deletable=False,
            editable=False,
            details=True,
            create=False,
            searchable=False,
            paginate=10,
            csv=False,
            sortable=False
        )


    if auth.is_logged_in():
        knotstock_grid = SQLFORM.grid(
            knotstocks_to_show,
            deletable=can_edit_record,
            fields=["knotstock"],
            #editable=can_edit_record,
            details=False,
            create=False,
            searchable=False,
            paginate=10,
            csv=False,
            sortable=False
        )
    else:
        knotstock_grid = SQLFORM.grid(
            knotstocks_to_show,
            deletable=False,
            editable=False,
            details=True,
            create=False,
            searchable=False,
            paginate=10,
            csv=False,
            sortable=False
        )

    return dict(
        #search_next=search_next,
        #search_results=search_results,
        flower_grid=flower_grid,
        knotstock_grid=knotstock_grid,
        updated_content="Data for: " + keyword
    )


def showcolsrootstocks():
    # Assuming 'id' is the ID of the record you want to edit
    record_id = session.rootstock_id  # Replace with the actual ID of the record to be edited

    # Fetch the record from the database
    record = db.rootstock(record_id)

    # Define the fields to display in the edit form
    #editfields = ['name', 'ICD9', 'data_type']
    editfields = ['name']
    # Create an edit form for the specified record with custom submit button and styles
    edit_form = SQLFORM(db.rootstock, record, fields=editfields, submit_button='Save', _style='font-size: 3vh;')

    if 'pond' in db.rootstock.fields:  # Check if 'pond' is a field in db.rootstock
        edit_form.vars.pond = session.pond_id
    # Check if form is submitted and process the form data
    if edit_form.process().accepted:
        # Form was successfully submitted and data updated in the database
        response.flash = 'Record updated successfully'

    # Prepopulate the 'pond' field with session.pond_id (assuming session.pond_id exists)
    if 'pond' in edit_form.vars:
        edit_form.vars.pond = session.pond_id


    #fields = ['name','ICD9','data_type']
    fields = ['name']
    create_form = SQLFORM(db.rootstock, submit_button='Grow the new plant', fields=fields,
                      _style='font-size: 3vh;', _id='create_rootstock',
                      _onsubmit="refreshDiv();")
    # Prepopulate the pond field with session.pond_id
    db.rootstock.pond.default = session.pond_id  # Set default value at DB levelcreate_form.vars.pond = session.pond_id

    if create_form.process().accepted:
        print("Form submission accepted!")  # Debugging
        response.flash = 'Record created successfully'
        response.js = "document.getElementById('rootstockpond').reload(true);"
    elif create_form.errors:
        print("Form errors:", create_form.errors)  # Debugging
        response.flash = 'Form has errors: ' + str(create_form.errors)
        response.status = 400
        

#OLD
    # Create the form
    new_flower = SQLFORM(db.flower, fields=['name', 'flower_type', 'growing_place'], submit_button='Create')

    # Process the form submission
    if new_flower.process().accepted:
        response.flash = 'Record created successfully'
    elif new_flower.errors:
        response.flash = 'Form has errors'
        response.status = 400  # Indicate a bad request

        # Check if the error is due to a duplicate name
        if 'name' in new_flower.errors:
            response.flash = 'This name is already registered. Please choose another.'

    # Adjust element targeting if necessary
    new_flower_field = new_flower.element('select[name="name"]')






    flowerfields = ['flower']

    # Create the SQLFORM instance with specified fields and submit button
    create_flower = SQLFORM(db.flower_list, submit_button='Create', fields=flowerfields)

    # Set the 'rootstock' variable in create_next to session.rootstock_id
    create_flower.vars.rootstock = session.rootstock_id

    # Process form submission
    if create_flower.process().accepted:
        # Form data was submitted and accepted
        response.flash = 'Record created successfully'
        # Additional actions after successful form submission can be placed here

    elif create_flower.errors:
        # Form has validation errors
        response.status = 400  # Set response status to indicate bad request if there are errors

    # Output the form element for 'knotstock' field
    flower_field = create_flower.element('select[name="flower"]')


    # Define function to check if a record can be edited by the current user
    def can_edit_record(row):
        if auth.is_logged_in():
            return row.created_by == auth.user.id
        return False





    # Fetch knotstocks based on the session.pond_id

    nextfields = ['knotstock']

    # Create the SQLFORM instance with specified fields and submit button
    create_next = SQLFORM(db.knotstock_list, submit_button='Create', fields=nextfields)

    # Set the 'rootstock' variable in create_next to session.rootstock_id
    create_next.vars.rootstock = session.rootstock_id

    # Process form submission
    if create_next.process().accepted:
        # Form data was submitted and accepted
        response.flash = 'Record created successfully'
        # Additional actions after successful form submission can be placed here

    elif create_next.errors:
        # Form has validation errors
        response.status = 400  # Set response status to indicate bad request if there are errors

    # Output the form element for 'knotstock' field
    knotstock_field = create_next.element('select[name="knotstock"]')

    # The form 'create_next' now contains the custom dropdown menu for 'knotstock'


    # Create a grid control.
    try:
        flowers_to_show = (db.flower_list.rootstock == session.rootstock_id)
    except:
        flowers_to_show = None  # Handle the case when session.rootstock_id is not set
    try:
        knotstocks_to_show = (db.knotstock_list.rootstock == session.knotstocks_id)
    except:
        knotstocks_to_show = None  # Handle the case when session.rootstock_id is not set        
    #For the search function:
    keyword = request.vars.colnodkeyword or ''

    if keyword:
        rootstocks_to_show = db((db.rootstock.pond == session.pond_id) & (db.rootstock.name.contains(keyword)))
    else:
        rootstocks_to_show = db(db.rootstock.pond == session.pond_id)



#2025-03-08
    def display_pond_name(row):
        return A(
        #row.name,
        #_style="left:1vw;color:blue;font-weight:bold;opacity:0.5;width:35vw;height:2em;position:absolute;margin:-0.5em -0.5em 0 1em;background-color:rgba(255,255,0,0.5);  display: block;  width: auto; height:auto;  text-decoration: none;   color: inherit; padding: 0;box-sizing: border-box; ",
        #callback=URL('found_rootstock', args=[int(row.id)])
    #NEW:
            row.name,
            _style="color:blue;font-weight:bold;text-decoration:none;cursor:pointer;",
            _onclick=f"toggleDiv('rootstock_{row.id}')"
        )
    rootstock_rows = rootstocks_to_show.select()
    rootstock_divs = DIV(
        *[DIV(f"Details for {row.name}", _class="ootstocklings", _id=f"rootstock_{row.id}", _style="display:none;") for row in rootstock_rows]
    )

    script = SCRIPT(
        """
        function toggleDiv(id) {
            let elements = document.getElementsByClassName('rootstocklings');
            for (let i = 0; i < elements.length; i++) {
                elements[i].style.display = 'none';
            }
            var div = document.getElementById(id);
            div.style.display = "block";
        }
        """
    )


    # Display the grid based on user authentication status
    if auth.is_logged_in():
        flower_grid = SQLFORM.grid(
            flowers_to_show,
            fields = [db.flwoer.name],
            deletable=can_edit_record,
            #deletable=True,
            editable=False,
            details=False,
            create=False,
            searchable=False,
            paginate=10,
            csv=False,
            sortable=True
        )
    else:
        flower_grid = SQLFORM.grid(
            flowers_to_show,
            fields = [db.flwoer.name],
            deletable=False,
            editable=False,
            details=False,
            create=False,
            searchable=False,
            paginate=10,
            csv=False,
            sortable=True
        )

    # Display the grid based on user authentication status
    if auth.is_logged_in():
        rootstock_grid = SQLFORM.grid(
            rootstocks_to_show,
            fields = [db.rootstock.name],
            deletable=can_edit_record,
            #deletable=True,
            editable=False,
            details=False,
            create=False,
            searchable=False,
            paginate=10,
            csv=False,
            sortable=True
        )
    else:
        rootstock_grid = SQLFORM.grid(
            rootstocks_to_show,
            fields = [db.rootstock.name],
            deletable=False,
            editable=False,
            details=False,
            create=False,
            searchable=False,
            paginate=10,
            csv=False,
            sortable=True
        )



    if auth.is_logged_in():
        knotstock_grid = SQLFORM.grid(
            knotstocks_to_show,
            deletable=can_edit_record,
            fields=[db.knotstock_list.knotstock],  # Use db.table.field
            details=False,
            create=False,
            searchable=False,
            paginate=10,
            csv=False,
            sortable=False
        )
    else:
        knotstock_grid = SQLFORM.grid(
            knotstocks_to_show,
            deletable=False,
            details=False,
            create=False,
            searchable=False,
            paginate=10,
            csv=False,
            sortable=False
        )        

    return dict(
        knotstock_grid=knotstock_grid,
        flower_grid=flower_grid,
        edit_form=edit_form,
        create_form=create_form,
        rootstock_divs=rootstock_divs,
        script=script,
        rootstock_grid=rootstock_grid,
    )





def found_coll():
    rootstocks_to_show = db(db.rootstock.pond == session.pond_id).select()
    nodes = []
    links = []
    session.pond_id = request.args(0)
    for index, the_rootstock in enumerate(rootstocks_to_show, start=1):
        nodes.append({"id": index, "label": the_rootstock.name, "x": 75, "y": 75 * index})

    # Build the list
    for index, the_rootstock in enumerate(rootstocks_to_show, start=1):
        # Build the graph string
        flowers_to_show = db(db.knotstock_list.rootstock == str(the_rootstock.id)).select()
        for flower_show in flowers_to_show:
            for index2, rootstock2 in enumerate(rootstocks_to_show, start=1):
                if rootstock2.id == flower_show.knotstock:
                    links.append({"source": index, "target": index2})

    # Pass rootstocks and links to the view
    response.js = "reloadFoundCollView();"
    return response.render('default/found_coll.html', {'nodes': nodes, 'links': links}, ajax=True)


def showflowchart():
    # Retrieve record ID from the URL
    record_id = request.args(0)

    # Fetch the record from the database
    pond = db.pond(record_id)  # Assuming 'crows' is your table name
    session.pond_id = record_id
#    found_coll()
    # Check if record exists
    if not pond:
        raise HTTP(404, "Record not found")

    response.js = "alert('Hello from found_coll!');"
    rootstocks_to_show = db(db.rootstock.pond == session.pond_id).select()
    rootstocks = []
    links = []
    for index, the_rootstock in enumerate(rootstocks_to_show, start=1):
        rootstocks.append({"id": index, "label": the_rootstock.name, "x": 75, "y": 75 * index})

    # Build the list
    for index, the_rootstock in enumerate(rootstocks_to_show, start=1):
        # Build the graph string
        knotstocks_to_show = db(db.knotstock_list.rootstock == str(the_rootstock.id)).select()
        for next_show in knotstocks_to_show:
            for index2, rootstock2 in enumerate(rootstocks_to_show, start=1):
                if rootstock2.id == next_show.knotstock:
                    links.append({"source": index, "target": index2})

    return response.render('default/showflowchart.html', {'rootstocks': rootstocks, 'links': links}, ajax=True)

def check_record_permission(record_id):
    record = db.pond(record_id)
    if record and record.created_by == auth.user_id:
        return True
    return False


def showponds():
    keyword = request.vars.colkeyword
    if keyword:
        crows = db(db.pond.name.contains(keyword))
    else:
        # If no keyword, fetch all ponds
        crows = db.pond

    def can_edit_record(row):
        return check_record_permission(row.id)

    def found_coll_link(row):
        #response.js = ("document.getElementById('popupI').style.display='block';")
        return A('Select', callback=URL('found_coll', args=[row.id]))

    if auth.is_logged_in():
        return dict(pond_grid=SQLFORM.grid(
            crows,
            csv=False,
            sortable=True,
            paginate=10,
            deletable=can_edit_record,
            editable=can_edit_record,
            details=False,
            create=False,
            searchable=False,
            links = [lambda row: A('Show pond', _href=URL('default', 'showflowchart', args=[row.id]))],
            #links=[lambda row: found_coll_link(row)],  # Use the modified lambda function
            formname='colls',
        ))
    else:
        return dict(pond_grid=SQLFORM.grid(
            crows,
            csv=False,
            sortable=True,
            paginate=10,
            deletable=False,
            editable=False,
            details=False,
            create=False,
            searchable=False,
            links = [lambda row: A('Show flowchart', _href=URL('default', 'showflowchart', args=[row.id]))],
            #links=[lambda row: found_coll_link(row)],  # Use the modified lambda function
            formname='colls',
        ))





def found_rootstock():
    # Get the ID from the URL parameter and store it in the session
    response.js="alert('test');"
    the_id = request.args(0)
    session.rootstock_id = int(the_id)  # Convert ID to integer and store in session
    #response.js = "window.location.reload();"
#nextrootstock
    response.js = "document.getElementById('left').reload(true);"
    #response.js = "document.getElementById('rootstockpond').reload(true);"


def chosen_rootstock():

    session.rootstock_id = int(the_id[0])

###???
    response.js = "web2py_component('%s','showcolsrootstocks.load')" % URL('default','showcolsrootstocks')
    response.js = 'window.location = "%s";' % URL('default','index')

    #import gluon.contenttype
    #response.headers['Content-Type']=gluon.contenttype.contenttype('.js')

    return #('document.getElementById("nextrootstock").style.display="block";')



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
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


@auth.requires_login()
def create_rootstock():
    form = SQLFORM(db.rootstock)
    if form.process().accepted:
        return "rootstock created successfully!"
    elif form.errors:
        return "Form has errors: " + str(form.errors)
    return "Unexpected error"

def update_rootstock_id():
    if request.vars.rootstock_id:
        try:
            session.rootstock_id = int(request.vars.rootstock_id)
            return response.json({"success": True, "rootstock_id": session.rootstock_id})
        except ValueError:
            return response.json({"success": False, "error": "Invalid rootstock_id"})
    return response.json({"success": False, "error": "No rootstock_id provided"})