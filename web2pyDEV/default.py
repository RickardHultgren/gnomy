# -*- coding: utf-8 -*-
from gluon import SQLFORM, URL, DIV, A, H2
from gluon.tools import Auth

# Initialize authentication system
auth = Auth(db)
auth.define_tables(username=False, signature=False)

def index():
    """ 
    Home page: Displays ponds and rootstocks owned by the logged-in user.
    Allows users to add new ponds and rootstocks.
    """
    if not auth.user:
        return dict(message="Please log in", form=None, grid=None, rootstock_form=None, rootstock_grid=None, pond_container=None, rootstock_container=None)

    # ---- Ponds Section ----
    db.pond.created_by.default = auth.user.id
    db.pond.created_by.writable = False
    db.pond.created_by.readable = False

    # Form for adding ponds
    form = SQLFORM(db.pond).process()

    # Fetch user's ponds
    pond_query = (db.pond.created_by == auth.user.id)
    pond_fields = [db.pond.name]

    # Pass selected pond ID via URL
    pond_links = [
        dict(header='', body=lambda row: A(row.name, 
                                           _href=URL('default', 'index', vars={'selected_pond_id': row.id}), 
                                           _class="pond-link"))
    ]

    # Grid for displaying ponds
    pond_grid = SQLFORM.grid(pond_query, fields=pond_fields, links=pond_links, create=False, editable=False, deletable=False,
                             details=False, paginate=10, csv=False, user_signature=False)

    # ---- Rootstocks Section ----
    db.rootstock.created_by.default = auth.user.id
    db.rootstock.created_by.writable = False
    db.rootstock.created_by.readable = False

    # Form for adding rootstocks
    rootstock_form = SQLFORM(db.rootstock).process()

    # ✅ Show rootstocks only if a pond is selected
    selected_pond_id = request.vars.selected_pond_id
    if selected_pond_id:
        rootstock_query = (db.rootstock.pond == selected_pond_id)
    else:
        rootstock_query = (db.rootstock.id == None)  # No rootstocks will be shown

    rootstock_fields = [db.rootstock.name]
    rootstock_links = [
        dict(header='', body=lambda row: A(row.name, _href=URL('default', 'rootstock', args=[row.id]), _class="rootstock-link"))
    ]

    # Grid for displaying rootstocks
    rootstock_grid = SQLFORM.grid(rootstock_query, fields=rootstock_fields, links=rootstock_links, create=False, editable=False, deletable=False,
                                  details=False, paginate=10, csv=False, user_signature=False)

    return dict(message=None, form=form, grid=pond_grid, rootstock_form=rootstock_form, rootstock_grid=rootstock_grid, pond_container=DIV(), rootstock_container=DIV())


def rootstock():
    """ Displays a selected rootstock's details. """
    rootstock_id = request.args(0, cast=int)
    rootstock = db.rootstock(rootstock_id) or redirect(URL('index'))

    return dict(rootstock=rootstock)
