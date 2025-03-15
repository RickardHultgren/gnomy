def get_rootstocks():
    """Fetch all rootstocks from the database."""
    rootstocks = db(db.rootstock).select()
    result = [{"id": r.id, "name": r.name} for r in rootstocks]
    return response.json(dict(rootstocks=result))

def get_tendrils():
    """Fetch tendrils for a given rootstock_id."""
    rootstock_id = request.vars.rootstock_id
    if not rootstock_id:
        return response.json(dict(error="No rootstock_id provided"))

    tendrils = db(db.tendril.rootstock_id == rootstock_id).select()
    result = [{"name": t.name, "knotstock": t.knotstock_id} for t in tendrils]

    return response.json(dict(tendrils=result))

def add_tendril():
    """Add a new tendril to the database."""
    rootstock_id = request.vars.rootstock_id
    name = request.vars.name

    if not rootstock_id or not name:
        return response.json(dict(error="Missing rootstock_id or name"))

    db.tendril.insert(rootstock_id=rootstock_id, name=name)
    db.commit()

    return response.json(dict(success=True))
