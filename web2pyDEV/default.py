# -*- coding: utf-8 -*-

def index():
    if not auth.is_logged_in():
        return dict(message="please log in")

    # Pond form for creating new ponds
    pond_form = SQLFORM(db.pond).process()

    # Query user's ponds
    ponds = db(db.pond.created_by == auth.user_id).select()

    return dict(pond_form=pond_form, ponds=ponds)

def get_rootstocks():
    """Returns the rootstocks for a given pond ID (AJAX call)."""
    pond_id = request.vars.pond_id
    if not pond_id:
        return "Invalid pond ID"

    rootstocks = db(db.rootstock.pond == pond_id).select()
    return dict(rootstocks=rootstocks)

def add_rootstock():
    """Handles adding a new rootstock to a pond via AJAX."""
    pond_id = request.vars.pond_id
    name = request.vars.name

    if not pond_id or not name:
        return "Invalid input"

    db.rootstock.insert(pond=pond_id, name=name, created_by=auth.user_id)
    return "Rootstock added successfully"
