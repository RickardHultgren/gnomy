from gluon.http import redirect
import json
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
#def index():
#    response.flash = T("Hello World")
#    return dict(message=T('Welcome to web2py!f'))

# Use layout.html to create the "master" page.
# View will call view file showtasks.html.g

#mymodule = local_import(filtering)
#response.files.append('https://d3js.org/d3.v3.min.js')

session.the_id = int()
if not session.coll_id:
    session.coll_id = int(0)


if not session.node_id:
    session.node_id = int(0)

if not session.graph_string:
    session.graph_string = "digraph { "
#session.graph_string = "digraph { "


if not session.nodes_pass:
    session.nodes_pass = dict()

if not session.len_nodes_pass :
    session.len_nodes_pass

if not session.new_graph :
    session.new_graph = 0

def index():
    return locals()




def add_collection():
    # Check if the user is logged in
    if not auth.is_logged_in():
        redirect(URL('default', 'user', args='login'))

    # Process the form submission
    if request.method == 'POST':
        # Insert data into the 'collection' table based on form input
        inserted_id = db.collection.insert(**request.post_vars)

        response.flash = f'Collection added successfully with ID: {inserted_id}'
        redirect(URL('default', 'index'))

    # Create an empty form
    form = SQLFORM(db.collection)

    response.js="document.getElementById('collchoice').reload(true);"
    return dict()

def add_node():
    # Check if the user is logged in
    if not auth.is_logged_in():
        redirect(URL('default', 'user', args='login'))

    # Process the form submission
    if request.method == 'POST':
        # Insert data into the 'collection' table based on form input
        inserted_id = db.node.insert(**request.post_vars)

        #response.flash = f'Node added successfully with ID: {inserted_id}'
        #redirect(URL('default', 'index'))
        #showcolsnodes()
    # Create an empty form
    form = SQLFORM(db.next_node)


    # Assuming the form has been successfully processed
    response.flash = 'Node added successfully'

    # You can redirect to another page or reload the index view
    # Example: redirect to the index page
    redirect(URL('default', 'index'))

    # If you prefer to reload the content without redirecting, you can use AJAX
    # Example: return a JSON response indicating success, and handle it in your JavaScript
    return response.json({'success': True})
    #return dict()


def addnext():
    # Check if the user is logged in
    if not auth.is_logged_in():
        redirect(URL('default', 'user', args='login'))

    # Process the form submission
    if request.method == 'POST':
        # Extract data from the form
#        node_id = request.vars.node
        next_node_id = request.vars.next_node

        # Insert a new record into the 'next_node_list' table
        inserted_id = db.next_node_list.insert(
            node=session.node_id,
            next_node=next_node_id,
            created_by=auth.user.id,
        )

        # Optionally, you can add a flash message or redirect to another page
        response.flash = f'Next node added successfully with ID: {inserted_id}'
        response.js="document.getElementById('nextspec').reload(true);"
        response.js="document.getElementById('foundcoll').reload(true);"
        #redirect(URL('default', 'index'))

    # Render the view or redirect if needed
    return dict()



def add_next_OLD():
    # Check if the user is logged in
    if not auth.is_logged_in():
        redirect(URL('default', 'user', args='login'))

    # Process the form submission
    if request.method == 'POST':
        # Get the names of the nodes from the form
        selected_nodes = request.vars.node

        # Handle the case where multiple nodes are selected
        if isinstance(selected_nodes, list):
            node_ids = [int(node_id) for node_id in selected_nodes]
        else:
            # Handle the case where only one node is selected
            node_ids = [int(selected_nodes)]

            ####
        # Insert data into the 'collection' table based on form input
        node = db(db.node.name == node_name).select(db.node.id).first()
        next_node = db(db.node.name == next_node_name).select(db.node.id).first()

        inserted_id = db.node.insert(**request.post_vars)

        #response.flash = f'Node added successfully with ID: {inserted_id}'
        #redirect(URL('default', 'index'))
        #showcolsnodes()
    # Create an empty form
    form = SQLFORM(db.next_node)


    # Assuming the form has been successfully processed
    response.flash = 'Node added successfully'

    # You can redirect to another page or reload the index view
    # Example: redirect to the index page
    redirect(URL('default', 'index'))

    # If you prefer to reload the content without redirecting, you can use AJAX
    # Example: return a JSON response indicating success, and handle it in your JavaScript
    return response.json({'success': True})
    #return dict()



'''

# controllers/default.py

def insert_equation_components(equation_id, components):
    for component in components:
        if component['type'] == 'number':
            component_id = db.numbers.insert(value=component['value'])
        else:
            component_id = db.operators.insert(value=component['value'])

        db.equation_components.insert(
            equation_id=equation_id,
            component_type=component['type'],
            component_id=component_id,
            parenthesis=component.get('parenthesis')
        )

# Example usage
equation_id = db.equation.insert(equation_name='Example Equation', equation_description='Example equation with parentheses')
components = [
    {'type': 'number', 'value': 5},
    {'type': 'operator', 'value': '+'},
    {'type': 'open_parenthesis', 'parenthesis': 'open'},
    {'type': 'number', 'value': 10},
    {'type': 'operator', 'value': '*'},
    {'type': 'number', 'value': 2},
    {'type': 'close_parenthesis', 'parenthesis': 'close'}
]
insert_equation_components(equation_id, components)

def evaluate_equation(equation_id):
    components = db(db.equation_components.equation_id == equation_id).select(orderby=db.equation_components.id)

    # Define a function to recursively evaluate the equation
    def evaluate_recursive(components, index):
        # Implementation of recursive equation evaluation
        pass

    result = evaluate_recursive(components, 0)
    return result

# Example usage
equation_result = evaluate_equation(equation_id)










'''






#Test function:

def check():#(name):
    import gluon.contenttype
    id_list = request.args
    response.headers['Content-Type']=gluon.contenttype.contenttype('.js')
    #return ('alert("%s");'% id_list)
'''    message=request.args(1)

    collectionnode = (db.node.collection == session.the_id)
    tables = []

    for t in db.node:
        tables.append({'name': '%s' % (t.name)})
    ul_main = UL(_class='nav nav-list')
    for t in tables:
        ul_main.append(A(t['name'], _onclick=URL(r=request,f='check',args= t['name']), _style="background-color:yellow"))
    return ul_main
'''
def addnext():
    # Ensure user is authenticated
    if not auth.user:
        raise HTTP(403, "Authentication required")

    # Extract data from the AJAX request
    nextname = request.vars.nextname

    # Ensure session.node_id is set and valid
    if 'node_id' not in session or not session.node_id:
        raise HTTP(400, "Invalid session node_id")

    # Retrieve the name of the current node (assuming 'node' table and 'name' field)
    current_node = db.node[session.node_id]
    if not current_node:
        raise HTTP(400, "Node not found in the database")

    name = current_node.name

    # Insert a new record into the 'next_node_list' table
    nextnode_id = db.next_node_list.insert(
        name=name,
        nextname=nextname,
        created_by=auth.user.id,
    )

    # Reload the 'nodecoll' element after successful insertion
    response.js = "document.getElementById('nodecoll').reload(true);"
    response.js = "document.getElementById('foundcoll').reload(true);"

    # Return a JSON response indicating success and the ID of the inserted record
    return response.json(dict(success=True, id=nextnode_id))







    #if auth.is_logged_in():
        #return dict(
            #next_node_grid=SQLFORM.grid(
                #nodes_to_show, user_signature=False, csv=False, searchable=True,
        #sortable=True,
        #paginate=20,
        #deletable=True,
        #editable=True,
        #details=True,
        #create=True,
                                #links = [lambda row: A('Select', callback=URL('selected_node',args=[row.id]))],#, callback=URL('check',args=[row.id]))]
    #formname='collections')
     #       )
    #else:
     #   return dict(
      #      next_node_grid=SQLFORM.grid(
       #         nodes_to_show, user_signature=False, csv=False, searchable=True,
        #sortable=True,
        #paginate=20,
        #deletable=False,
        #editable=False,
        #details=True,
        #create=False,
                                #links = [lambda row: A('Select', callback=URL('selected_node',args=[row.id]))],#, callback=URL('check',args=[row.id]))]
       #formname='collections')
       #     )

def nodedelete():
    record_id = session.node_id
    db(db.node.id == record_id).delete()

    #response.js = "document.getElementById('nodecoll').reload(true);"
    response.js = "document.getElementById('nodecoll').reload(true);"
    response.js = "document.getElementById('foundcoll').reload(true);"
    return #"Record deleted successfully"

def node_next_delete():
    record_id = request.vars.record_id
    # Perform delete operations on multiple tables
    nexts_to_delete = db(db.next_node_list.node==session.record_id)
    #db.table1(db.table1.id == record_id).delete()
    #db.table2(db.table2.id == record_id).delete()
    for next_del in nexts_to_delete:

        db.next_node_list(db.next_node_list.id == next_del.id).delete()
    db.node(db.node.id == record_id.id).delete()

    # Add more delete operations for other tables if needed

def shownextnodes():
    # Create a grid control.
    try:
        nexts_to_show = (db.next_node_list.node == session.node_id)
    except:
        nexts_to_show = None  # Handle the case when session.node_id is not set

    # Create the search form using SQLFORM
    #search_next = SQLFORM(db.next_node, submit_button='Search')
    #search_next.custom['_id'] = 'search_next_id'  # Set the ID attribute for the submit button

    # Process the form submission and retrieve search results
    #search_results = None
    #if request.vars and search_next.process().accepted:
    #    query = db.next_node.name.contains(search_next.vars.name)
    #    search_results = db(query).select()

    # Define function to check if a record can be edited by the current user
    def can_edit_record(row):
        if auth.is_logged_in():
            return row.created_by == auth.user.id
        return False

    # Define function to create a delete link for a node record
    def can_delete_node(row):
        if auth.is_logged_in() and row.created_by == auth.user.id:
            delete_url = URL('default', 'node_delete', args=[row.id])
            return A('Delete!', 
                    _style="height:1em;", 
                    _href=delete_url, 
                    _class='btn btn-danger delete-btn',  # Use class instead
                    _data=dict(node_id=row.id))  # Store ID in data attribute
        return None
        
    # Display the grid based on user authentication status
    if auth.is_logged_in():
        next_node_grid = SQLFORM.grid(
            nexts_to_show,
            deletable=can_edit_record,
            fields=["next_node"],
            #editable=can_edit_record,
            details=False,
            create=False,
            searchable=False,
            paginate=10,
            csv=False,
            sortable=False
        )
    else:
        next_node_grid = SQLFORM.grid(
            nexts_to_show,
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
        next_node_grid=next_node_grid
    )

#########




def showcolsnodes():
    # Assuming 'id' is the ID of the record you want to edit
    record_id = session.node_id  # Replace with the actual ID of the record to be edited

    # Fetch the record from the database
    record = db.node(record_id)

    # Define the fields to display in the edit form
    #editfields = ['name', 'ICD9', 'data_type']
    editfields = ['name']
    # Create an edit form for the specified record with custom submit button and styles
    edit_form = SQLFORM(db.node, record, fields=editfields, submit_button='Save', _style='font-size: 3vh;')

    if 'collection' in db.node.fields:  # Check if 'collection' is a field in db.node
        edit_form.vars.collection = session.coll_id
    # Check if form is submitted and process the form data
    if edit_form.process().accepted:
        # Form was successfully submitted and data updated in the database
        response.flash = 'Record updated successfully'

    # Prepopulate the 'collection' field with session.coll_id (assuming session.coll_id exists)
    if 'collection' in edit_form.vars:
        edit_form.vars.collection = session.coll_id


    #fields = ['name','ICD9','data_type']
    fields = ['name']
    create_form = SQLFORM(db.node, submit_button='Create', fields=fields,
                      _style='font-size: 3vh;', _id='create_node',
                      _onsubmit="refreshDiv(); return false;")

    # Prepopulate the collection field with session.coll_id
    create_form.vars.collection = session.coll_id


    # Set dropdown options for the 'collection' field
    #create_form.custom.widget.collection = SQLFORM.widgets(thenode.name)


    # Define a custom widget function for the "collection" field
    #def custom_collection_widget(field, value):
        # Get the value of the field
    #    field_value = value if value is not None else field.default

        # Generate a div element to display the field value
    #    return DIV(field_value, _class='readonly-div')

    # Set the "collection" field widget to the custom div widget
    #create_form.custom.widget.collection = lambda field, value: custom_collection_widget(field, value)




    #create_form.custom['_id'] = 'submit_button_id'  # Set the ID attribute for the submit button

    if create_form.process().accepted:
            # Form data was submitted and accepted
            # Perform necessary actions here, e.g., save data to database
            #response.flash = 'Record created successfully'
            response.js = "document.getElementById('nodecoll').reload(true);"
            # Optional: Do not redirect or return a response if you want to stay on the same page
            # Instead, display a success message or update the current view
            pass

    elif create_form.errors:
            # Form has validation errors
            response.status = 400  # Bad request status if form has errors
    #if auth.is_logged_in():
    #    create_form = SQLFORM(db.node, submit_button='Create')
    #    create_form.custom.submit = 'SuBmIt'
    #    create_form.custom['_id'] = 'submit_button_id'  # Set the ID attribute for the submit button

    #    if create_form.process().accepted:
    #        # Form data was submitted and accepted
    #        # Perform necessary actions here, e.g., save data to database
    #        response.flash = 'Record created successfully'

    #        # Optional: Do not redirect or return a response if you want to stay on the same page
    #        # Instead, display a success message or update the current view
    #        pass

    #    elif create_form.errors:
            # Form has validation errors
    #        response.status = 400  # Bad request status if form has errors


    #For the search function:
    keyword = request.vars.colnodkeyword or ''
    if keyword:
        nodes_to_show = db((db.node.collection == session.coll_id) and (db.node.name.contains(keyword)))
    else:
        # If no keyword, fetch all collections
        nodes_to_show = db(db.node.collection == session.coll_id)

    #nodes_to_show = db.node
    #nodes_to_show = db.node
    #next_nodes_to_show = db.next_node

    #if auth.is_logged_in():
    #    my_record_id = request.args(0)
    #    edit_form = SQLFORM(db.node, record=my_record_id)
    #    #edit_form = SQLFORM(db.node, submit_button='Edit')
    #    if edit_form.process().accepted:
    #        response.js = "document.getElementById('edit-form-container').style.display = 'block';"
    #        my_record_id = request.args(0)  # Get the record ID from the URL
    #        record = db.node(my_record_id)
            # Form data was submitted and accepted, perform necessary actions here
    #        response.flash = 'Record edited successfully'

    #def can_edit_record(row):
        #return check_record_permission(row.id)

    #def can_edit_record(row):
    #    # Check if the user is logged in
    #    if auth.is_logged_in():
    #        # Check if the record was created by the logged-in user
    #        return row.created_by == auth.user.id
    #    else:
    #        return False

    #def can_delete_record(row):
    #    # Check if the user is logged in
    #    if auth.is_logged_in():
    #        # Check if the record was created by the logged-in user
    #        if row.created_by == auth.user.id:
    #            # Return the URL for deleting the record
    #            delete_url = URL('default', 'node_delete', args=[row.id])
    #            return A('Delete', _href=delete_url, _class='btn btn-danger', _data=dict(confirm="Are you sure?"))
    #    return None

    def display_collection_name(row):
        #response.js=("alert(%s)" % "row"+row)
        #now_nodes=dict
        #for now_nodes in db(db.node.collection == session.coll_id):
            #for now_node in now_nodes:
                #return A;(now_node.name, _href=URL('found_node', args=[row.id]))
        #return A(row.name,  callback=URL('found_node', args=[row.id]))#, _href=URL('found_node', args=[row.id]))
        return A(
        row.name,
        _style="left:1vw;color:blue;font-weight:bold;opacity:0.5;width:35vw;height:2em;position:absolute;margin:-0.5em -0.5em 0 1em;background-color:rgba(255,255,0,0.5);  display: block;  width: auto; height:auto;  text-decoration: none;   color: inherit; padding: 0;box-sizing: border-box; ",
        callback=URL('found_node', args=[int(row.id)])
    )
# Modify the links parameter to use the custom function to display collection names as links
# Generate the SQLFORM.grid with customized parameters
    #response.view = 'default/showflowchart/' + str(session.coll_id)
    #response.view = 'default/layout.html'
    #page = request.vars.page or 1
    #colnodkeyword = request.vars.colnodkeyword or ''

    # Define pagination settings
    #items_per_page = 10
    #offset = (int(page) - 1) * items_per_page

    # Query to fetch nodes based on keyword and pagination
    #nodes_query = (db.node.name.contains(colnodkeyword)) if colnodkeyword else (db.node.id > 0)
    #nodes = db(nodes_query).select(limitby=(offset, offset + items_per_page))

    # Render the view with the fetched nodes
    # Retrieve next nodes based on session.coll_id
    # Assuming session, db, response, and SQLFORM are properly imported and initialized

    # Fetch next_nodes based on the session.coll_id

    nextfields = ['next_node']

    # Create the SQLFORM instance with specified fields and submit button
    create_next = SQLFORM(db.next_node_list, submit_button='Create', fields=nextfields)

    # Set the 'node' variable in create_next to session.node_id
    create_next.vars.node = session.node_id

    # Process form submission
    if create_next.process().accepted:
        # Form data was submitted and accepted
        response.flash = 'Record created successfully'
        # Additional actions after successful form submission can be placed here

    elif create_next.errors:
        # Form has validation errors
        response.status = 400  # Set response status to indicate bad request if there are errors

    # Output the form element for 'next_node' field
    next_node_field = create_next.element('select[name="next_node"]')

    # The form 'create_next' now contains the custom dropdown menu for 'next_node'


    # Create a grid control.
    try:
        nexts_to_show = (db.next_node_list.node == session.node_id)
    except:
        nexts_to_show = None  # Handle the case when session.node_id is not set

    # Create the search form using SQLFORM
    #search_next = SQLFORM(db.next_node, submit_button='Search')
    #search_next.custom['_id'] = 'search_next_id'  # Set the ID attribute for the submit button

    # Process the form submission and retrieve search results
    #search_results = None
    #if request.vars and search_next.process().accepted:
    #    query = db.next_node.name.contains(search_next.vars.name)
    #    search_results = db(query).select()


    # Display the grid based on user authentication status
    if auth.is_logged_in():
        next_node_grid = SQLFORM.grid(
            nexts_to_show,
            #fields=['next_node'],
            #deletable=can_edit_record,
            deletable=True,
            editable=False,
            details=False,
            create=False,
            searchable=False,
            paginate=10,
            csv=False,
            sortable=True
        )
    else:
        next_node_grid = SQLFORM.grid(
            nexts_to_show,
            #fields=['next_node'],
            deletable=False,
            editable=False,
            details=False,
            create=False,
            searchable=False,
            paginate=10,
            csv=False,
            sortable=True
        )



    return dict(
        #search_next=search_next,
        #search_results=search_results,
        edit_form=edit_form,
        create_form=create_form,
        create_next=create_next,
        next_node_grid=next_node_grid,
        cols_node_grid=SQLFORM.grid(
        nodes_to_show,


        #fields=[lambda row: display_collection_name(row)],
        fields = [db.node.name],
        #fields=[dbnode.name],
        csv=False,
        sortable=True,
        paginate=10,
        deletable=False,
        #editable=can_edit_record,  # Set editable based on the result of the function
        editable=False,
        details=False,
        create=False,
        #create=True,
        searchable=True,
        links=[lambda row: display_collection_name(row)],
    )

    )











    #if auth.is_logged_in():
    #    return dict(cols_node_grid=SQLFORM.grid(
#            nodes_to_show,
#            csv=False,
#            sortable=True,
#            paginate=10,
            #deletable=can_edit_record,
#            deletable=False,
#            editable=can_edit_record,  # Set editable based on the result of the function
#            details=True,
#            create=True,
#            searchable=False,

 #           links=[lambda row: can_delete_record(row), lambda row: A('Select', callback=URL('found_node', args=[row.id]))],
 #       ))
 #   else:
#        return dict(cols_node_grid=SQLFORM.grid(
#            nodes_to_show,
#            csv=False,
#            sortable=True,
#            paginate=10,
#            deletable=False,
#            editable=False,
#            details=True,
#            create=False,
#            searchable=False,
#            links=[lambda row: A('Select', callback=URL('found_node', args=[row.id]), _style="cursor:pointer; padding: 5px; background-color: lightblue; opacity:0.5; width: 35vw; border: 1px solid black;     position: absolute;     transform: translateY(-50%);   background-color: lightblue;     color: black;     text-decoration: none;     border: 1px solid black;    z-index: 1; ")],
                #links=[lambda row: A('Select', callback=URL('found_node', args=[row.id]))],
#        ))



def found_coll():
    # Extract the_id from request.args
    #the_id = request.args(0)


    # Set default values if session variables are not already set

    #try:
    #    session.coll_id = int(the_id)
    #except:
    #    pass


    # Retrieve nodes to show for the specified collection
    #response.js = "alert('%s')"%session.coll_id
    nodes_to_show = db(db.node.collection == session.coll_id).select()
    nodes = []
    links = []
    for index, the_node in enumerate(nodes_to_show, start=1):
        nodes.append({"id": index, "label": the_node.name, "x": 75, "y": 75 * index})

    # Build the list
    for index, the_node in enumerate(nodes_to_show, start=1):
        # Build the graph string
        nexts_to_show = db(db.next_node_list.node == str(the_node.id)).select()
        for next_show in nexts_to_show:
            for index2, node2 in enumerate(nodes_to_show, start=1):
                if node2.id == next_show.next_node:
                    links.append({"source": index, "target": index2})
    #response.js = 'alert("links '+links+'");'
    #response.js = "alert('AAA')"
    # Pass nodes and links to the view
    response.js = "reloadFoundCollView();"
    return response.render('default/found_coll.html', {'nodes': nodes, 'links': links}, ajax=True)


def showflowchart():
    # Retrieve record ID from the URL
    record_id = request.args(0)

    # Fetch the record from the database
    collection = db.collection(record_id)  # Assuming 'crows' is your table name
    session.coll_id = record_id
#    found_coll()
    # Check if record exists
    if not collection:
        raise HTTP(404, "Record not found")

    response.js = "alert('Hello from found_coll!');"
    nodes_to_show = db(db.node.collection == session.coll_id).select()
    nodes = []
    links = []
    for index, the_node in enumerate(nodes_to_show, start=1):
        nodes.append({"id": index, "label": the_node.name, "x": 75, "y": 75 * index})

    # Build the list
    for index, the_node in enumerate(nodes_to_show, start=1):
        # Build the graph string
        nexts_to_show = db(db.next_node_list.node == str(the_node.id)).select()
        for next_show in nexts_to_show:
            for index2, node2 in enumerate(nodes_to_show, start=1):
                if node2.id == next_show.next_node:
                    links.append({"source": index, "target": index2})
    #response.js = 'alert("links '+links+'");'
    #response.js = "alert('AAA')"
    # Pass nodes and links to the view

    # Render the details view with the record data
    #rendered_html = response.render('default/showflowchart.html', {'nodes': nodes, 'links': links}, ajax=True)
#
        # rn both data and rendered HTML
    #return dict(collection=collection, rendered_html=rendered_html)

    return response.render('default/showflowchart.html', {'nodes': nodes, 'links': links}, ajax=True)

def check_record_permission(record_id):
    record = db.collection(record_id)
    if record and record.created_by == auth.user_id:
        return True
    return False




def showcollections():
    keyword = request.vars.colkeyword
    if keyword:
        crows = db(db.collection.name.contains(keyword))
    else:
        # If no keyword, fetch all collections
        crows = db.collection

    def can_edit_record(row):
        return check_record_permission(row.id)

    def found_coll_link(row):
        #response.js = ("document.getElementById('popupI').style.display='block';")
        return A('Select', callback=URL('found_coll', args=[row.id]))

    if auth.is_logged_in():
        return dict(collection_grid=SQLFORM.grid(
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
        return dict(collection_grid=SQLFORM.grid(
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





def found_node():
    # Get the ID from the URL parameter and store it in the session
    #response.js="alert('test');"
    the_id = request.args(0)
    session.node_id = int(the_id)  # Convert ID to integer and store in session
    #response.js = "window.location.reload();"

    response.js = "document.getElementById('nodecoll').reload(true);"


def chosen_node():

    session.node_id = int(the_id[0])

###???
    response.js = "web2py_component('%s','showcolsnodes.load')" % URL('default','showcolsnodes')
    response.js = 'window.location = "%s";' % URL('default','index')

    #import gluon.contenttype
    #response.headers['Content-Type']=gluon.contenttype.contenttype('.js')

    return #('document.getElementById("nextnode").style.display="block";')


#def next_node_rquest():
#
#    return

# index.html view uses this








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
