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

#session.the_id = int()
#if not session.coll_id:
#    session.coll_id = int(0)


#if not session.node_id:
#    session.node_id = int(0)

#if not session.graph_string:
#    session.graph_string = "digraph { "
#session.graph_string = "digraph { "


def index():

    # Fetch database entries
    database_entries = {row.id: row.description for row in db(db.thedatabase).select()}
    
    # Fetch inventory data
    inventory = {
        "Relatedness": sorted([database_entries.get(1, "")]),
        "Competence": sorted([database_entries.get(3, "")]),
        "Autonomy": sorted([database_entries.get(2, "")])
    }
    
    # Fetch situation data
    situation = {
        "contexts": {
            "Home": [],
            "Work": [],
            "Hobby": [database_entries.get(4, ""), database_entries.get(5, "")]
        }
    }

    # Fetch situation links
    situation_links = {
        "1": {
            "from": [database_entries.get(4, "")],
            "to": [database_entries.get(5, "")]
        }
    }

    # Fetch ladder data
    ladder = {
        "ladder": {
            "1": [database_entries.get(1, "")],
            "2": [database_entries.get(1, "")],
            "3": [database_entries.get(1, "")],
            "4": [database_entries.get(1, "")]
        }
    }

    # Fetch autonomy subcategory
    autonomy_subcategory = {
        "subCategory": {
            "My": [database_entries.get(2, "")],
            "Borrowed": [],
            "Lent": []
        }
    }

    # Merge autonomy categories
    inventory["Autonomy"] = sorted(
        autonomy_subcategory["subCategory"]["My"]
        + autonomy_subcategory["subCategory"]["Borrowed"]
        + autonomy_subcategory["subCategory"]["Lent"]
    )

    # Matches selected (empty for now)
    matches_selected = []

    # Matches to do
    matches_to_do = [
        {"id": 1, "A": "itemA1", "thanks": "I did it!!!", "resultContext": "Result Context", "resultSituation": "Result Situation"}
    ]

    # Convert to JSON for JavaScript
    data = {
        "database": database_entries,
        "inventoryData": {"inventory": inventory},
        "situationData": situation,
        "situationLinks": situation_links,
        "ladderData": ladder,
        "autonomySubCategory": autonomy_subcategory,
        "matchesSelected": matches_selected,
        "matchesToDo": matches_to_do
    }

    # Pass the JSON data to the view
    return dict(data=XML(json.dumps(data, ensure_ascii=False)))





















@request.restful()  
def api():  
    # Set the response format to JSON
    response.view = "generic.json"  

    def GET(*args, **vars):  
        """Fetch all contexts and their situations."""
        
        # Retrieve all contexts from the database
        contexts = db(db.context.id > 0).select()  
        context_dict = {}  

        # Iterate over each context and fetch its related situations
        for context in contexts:  
            situations = db(db.situation.context_id == context.id).select()  
            context_dict[context.name] = [s.name for s in situations]  # Store situation names under their respective contexts

        return dict(contexts=context_dict)  # Return the dictionary containing contexts and their situations

    def POST(*args, **vars):  
        """Handle adding and deleting contexts and situations."""  
        
        action = vars.get("action")  # Get the action type from the request variables

        if action == "add_context":  
            # Add a new context if it does not already exist
            name = vars.get("name")  
            if name and not db(db.context.name == name).count():  
                db.context.insert(name=name)  # Insert new context into the database
                db.commit()  # Commit the changes to the database
                return dict(success=True)  # Return success response
            return dict(success=False, error="Context already exists or invalid name")  # Return error if context exists or name is invalid

        elif action == "delete_context":  
            # Delete a context and all its associated situations
            name = vars.get("name")  
            context = db(db.context.name == name).select().first()  # Retrieve the context by name
            if context:  
                db(db.situation.context_id == context.id).delete()  # Delete all situations linked to the context
                db(db.context.id == context.id).delete()  # Delete the context itself
                db.commit()  # Commit the changes
                return dict(success=True)  
            return dict(success=False, error="Context not found")  # Return error if context does not exist

        elif action == "add_situation":  
            # Add a new situation to an existing context
            context_name = vars.get("context")  
            situation_name = vars.get("name")  
            context = db(db.context.name == context_name).select().first()  # Retrieve the context by name
            if context and situation_name and not db((db.situation.name == situation_name) & (db.situation.context_id == context.id)).count():  
                db.situation.insert(name=situation_name, context_id=context.id)  # Insert new situation into the database
                db.commit()  # Commit the changes
                return dict(success=True)  
            return dict(success=False, error="Invalid context or situation already exists")  # Return error if the situation exists or context is invalid

        elif action == "delete_situation":  
            # Delete a situation from a context
            context_name = vars.get("context")  
            situation_name = vars.get("name")  
            context = db(db.context.name == context_name).select().first()  # Retrieve the context by name
            if context:  
                db((db.situation.name == situation_name) & (db.situation.context_id == context.id)).delete()  # Delete the situation in the given context
                db.commit()  # Commit the changes
                return dict(success=True)  
            return dict(success=False, error="Situation not found in context")  # Return error if situation does not exist

        return dict(success=False, error="Invalid request")  # Return error for unrecognized actions

    return locals()  # Expose the API endpoints (GET and POST)













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