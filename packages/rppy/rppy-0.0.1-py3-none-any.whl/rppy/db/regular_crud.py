def _filter_query(query, model, filters):
    for key, value in filters.items():
        query = query.filter(getattr(model, key) == value)
    return query


def create(session, model, params):
    obj = model(**params)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


def select(session, model, filters):
    query = session.query(model)
    query = _filter_query(query, model, filters)
    obj = query.all()
    return obj


def one(session, model, filters):
    query = session.query(model)
    query = _filter_query(query, model, filters)
    obj = query.one()
    return obj


def one_or_none(session, model, filters):
    query = session.query(model)
    query = _filter_query(query, model, filters)
    obj = query.one_or_none()
    return obj


def update(session, model, filters, params):
    obj = one(session, model, filters)
    for key, value in params.items():
        setattr(obj, key, value)
    session.commit()
    return obj


def delete(session, model, filters):
    obj = one(session, model, filters)
    session.delete(obj)
    session.commit()
    return obj
