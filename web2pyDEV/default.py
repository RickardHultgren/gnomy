from gluon.http import redirect
import json

session.the_id = int()
if not session.pond_id:
    session.pond_id = int(0)


if not session.rootstock_id:
    session.rootstock_id = int(0)

if not session.new_graph :
    session.new_graph = 0

def index():
    def can_edit_record(row):
        return check_record_permission(row.id)

    fields = ['name']
    create_pond = SQLFORM(db.pond, submit_button='Create a pond', fields=fields, _style='font-size: 3vh;', _id='create_pond', _onsubmit="refreshcollchoice();")

    # Ensure user is logged in before processing the form
    if auth.is_logged_in():
        if create_pond.process().accepted:
            # Explicitly set created_by field
            db.pond.update_or_insert(id=create_pond.vars.id, created_by=auth.user.id)
            response.flash = 'Pond created successfully!'
            redirect(URL('index'))  # Refresh to show new record
        elif create_pond.errors:
            response.flash = 'Please correct the errors in the form.'
    else:
        response.flash = 'You must be logged in to create a pond.'

    # Query only the ponds created by the logged-in user
    ponds_to_show = db(db.pond.created_by == auth.user.id) if auth.is_logged_in() else db(db.pond.id > 0)

    # Add a "Show pond" link to each row
    links = [lambda row: A('Show pond', _href=URL('default', 'showflowchart', args=[row.id]))]

    # Configure the grid
    pond_grid = SQLFORM.grid(
        ponds_to_show,
        deletable=can_edit_record if auth.is_logged_in() else False,
        editable=can_edit_record if auth.is_logged_in() else False,
        details=False,
        create=False,  # Use the form instead
        searchable=False,
        paginate=10,
        csv=False,
        sortable=False,
        links=links  # Add the links to the grid
    )

    return dict(create_pond=create_pond, pond_grid=pond_grid)





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
    flower_grid = SQLFORM.grid(
            flowers_to_show,
            deletable=can_edit_record if auth.is_logged_in() else False,
            fields=["knotstock"] if auth.is_logged_in() else False,
            editable=can_edit_record if auth.is_logged_in() else False,
            details=False if auth.is_logged_in() else False,
            create=False,
            searchable=False,
            paginate=10,
            csv=False,
            sortable=False
        )
    
    knotstock_grid = SQLFORM.grid(
            knotstocks_to_show,
            deletable=can_edit_record if auth.is_logged_in() else False,
            fields=["knotstock"] if auth.is_logged_in() else False,
            editable=can_edit_record if auth.is_logged_in() else False,
            details=False,
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
    #editfields = ['name']
    editfields = ['name', 'pond']
    # Create an edit form for the specified record with custom submit button and styles
    #edit_form = SQLFORM(db.rootstock, record, fields=editfields, submit_button='Save', _style='font-size: 3vh;')
    
    
    edit_form = SQLFORM(db.rootstock, record, fields=editfields, 
                        submit_button='Save', 
                        _style='font-size: 3vh;',
                        _formname='edit_form')

    if 'pond' in db.rootstock.fields:
        edit_form.vars.pond = session.pond_id  # This works *only if pond is in fields*


    # Check if 'pond' is a field in db.rootstock
    #if 'pond' in db.rootstock.fields:  
        #edit_form.vars.pond = session.pond_id

    # Prepopulate the 'pond' field with session.pond_id (assuming session.pond_id exists)
    #if 'pond' in edit_form.vars:
        #edit_form.vars.pond = session.pond_id
    #if session.pond_id and db(db.pond.id == session.pond_id).count():
    #    edit_form.vars.pond = session.pond_id
    #else:
    #    response.flash = 'Invalid pond reference!'


    # Check if form is submitted and process the form data
    if edit_form.process().accepted:
        # Form was successfully submitted and data updated in the database
        response.flash = 'Record updated successfully'


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
        


    # Create the flower form
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
    #def can_edit_record(row):
    #    if auth.is_logged_in():
    #        return row.created_by == auth.user.id
    #    return False

    def can_edit_record(row):
        if not row:
            return False  # Prevent errors
        if not hasattr(row, 'created_by'):
            return False  # If the field doesn't exist
        return row.created_by == auth.user.id

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
    flower_grid = SQLFORM.grid(
            flowers_to_show,
            fields = [db.flower.name] if auth.is_logged_in() else False,
            deletable=can_edit_record if auth.is_logged_in() else False,
            #deletable=True if auth.is_logged_in() else False,
            editable=False,
            details=False,
            create=False,
            searchable=False,
            paginate=10,
            csv=False,
            sortable=True
        )
    
    # Display the grid based on user authentication status
    rootstock_grid = SQLFORM.grid(
            rootstocks_to_show,
            fields = [db.rootstock.name] if auth.is_logged_in() else False,
            #fields=[db.rootstock.name, db.rootstock.created_by],  # Include created_by
            deletable=can_edit_record if auth.is_logged_in() else False,
            #deletable=True,
            editable=False,
            details=False,
            create=False,
            searchable=False,
            paginate=10,
            csv=False,
            sortable=True
        )



    knotstock_grid = SQLFORM.grid(
            knotstocks_to_show,
            deletable=can_edit_record if auth.is_logged_in() else False,
            fields=[db.knotstock_list.knotstock] if auth.is_logged_in() else False,  # Use db.table.field
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