# -*- coding: utf-8 -*-
from gluon import current

def index():
    """
    This function serves as the main page of the application.
    If the user is not logged in, it prompts them to log in.
    If the user is logged in, it displays a grid of their ponds and a form to add new ponds.
    """
    auth = current.auth
    db = current.db
    response = current.response
    request = current.request

    # Check if the user is logged in
    if not auth.user:
        message = "Please log in"
        form = None
        grid = None
    else:
        # Define the pond table if not already defined
        if not hasattr(db, 'pond'):
            db.define_table('pond',
                Field('name', 'string', requires=IS_NOT_EMPTY()),
                Field('user_id', 'reference auth_user', default=auth.user.id, readable=False, writable=False)
            )

        # Define the rootstock table if not already defined
        if not hasattr(db, 'rootstock'):
            db.define_table('rootstock',
                Field('pond_id', 'reference pond'),
                Field('name', 'string', requires=IS_NOT_EMPTY())
            )

        # Form to add a new pond
        form = SQLFORM(db.pond).process() if request.vars else None

        # Query to select ponds owned by the logged-in user
        query = (db.pond.user_id == auth.user.id)
        # Grid to display the user's ponds
        grid = SQLFORM.grid(query,
                            fields=[db.pond.name],
                            create=False,
                            editable=False,
                            deletable=True,
                            details=False,
                            selectable=None,
                            csv=False,
                            links=[
                                dict(header='Pond Name',
                                     body=lambda row: A(row.name, _href="#", _onclick="loadPond(%d)" % row.id))
                            ])

        # Handle form submission for adding a new pond
        if form and form.accepted:
            response.flash = 'New pond added!'
        elif form and form.errors:
            response.flash = 'Form has errors'

    return dict(message=message, form=form, grid=grid)

def pond():
    """
    This function loads the details of a specific pond, including its rootstocks and a form to add new rootstocks.
    It is called via AJAX when a pond name is clicked.
    """
    db = current.db
    request = current.request
    response = current.response

    # Get the pond ID from the URL
    pond_id = request.args(0, cast=int)
    if not pond_id:
        raise HTTP(400, "Invalid pond ID")

    # Retrieve the pond record
    pond = db.pond(pond_id) or redirect(URL('index'))

    # Form to add a new rootstock to the pond
    db.rootstock.pond_id.default = pond.id
    form = SQLFORM(db.rootstock).process() if request.vars else None

    # Query to select rootstocks associated with this pond
    query = (db.rootstock.pond_id == pond.id)
    # Grid to display the rootstocks of this pond
    grid = SQLFORM.grid(query,
                        fields=[db.rootstock.name],
                        create=False,
                        editable=False,
                        deletable=True,
                        details=False,
                        selectable=None,
                        csv=False)

    # Handle form submission for adding a new rootstock
    if form and form.accepted:
        response.flash = 'New rootstock added!'
    elif form and form.errors:
        response.flash = 'Form has errors'

    return dict(pond=pond, form=form, grid=grid)
