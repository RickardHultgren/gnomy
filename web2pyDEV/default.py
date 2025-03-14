# -*- coding: utf-8 -*-
from gluon import current

def index():
    """
    If the user is not logged in, display a message prompting them to log in.
    If logged in, display a grid of ponds owned by the user and handle pond creation.
    """
    auth = current.auth
    db = current.db
    response = current.response

    if not auth.user:
        # User is not logged in
        return dict(message="Please log in", grid=None, pond_form=None, rootstock_grids={})

    # User is logged in
    user_id = auth.user.id

    # Define the pond form
    pond_form = SQLFORM(db.pond)
    if pond_form.process().accepted:
        response.flash = 'New pond added'
    elif pond_form.errors:
        response.flash = 'Form has errors'

    # Display ponds owned by the user
    ponds = db(db.pond.owner == user_id).select()

    # Generate grids for each pond's rootstocks
    rootstock_grids = {}
    for pond in ponds:
        query = (db.rootstock.pond == pond.id)
        rootstock_grids[pond.id] = SQLFORM.grid(query, user_signature=False, create=True)

    return dict(message=None, grid=ponds, pond_form=pond_form, rootstock_grids=rootstock_grids)
