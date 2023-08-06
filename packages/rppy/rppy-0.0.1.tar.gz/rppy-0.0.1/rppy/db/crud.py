# Base crud functional
# For more difficult requests use append_only.py manually
# Warning! Fields like id, uid, created_at, is_deleted are required
# id, created_at, is_deleted is not allowed in WHERE statements
from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from . import append_only
from .base_class import Base

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


def _row2dict(row: Base) -> dict:
    """Convert SqlAlchemy object to dict"""
    return {column.name: getattr(row, column.name) for column in row.__table__.columns}


def _get_one_pure_dict(rows: List[Base]) -> dict:
    """Return one SqlAlchemy object, that was converted in dict.
       From dict removed service field like id, created_at
       If object not one, raise exception"""
    if len(rows) < 1:
        raise NoResultFound
    if len(rows) > 1:
        raise MultipleResultsFound
    obj = rows[0]
    obj_dict = _row2dict(obj)
    del obj_dict["id"]
    del obj_dict["created_at"]
    return obj_dict


def select(session: Session, model: Base, filters: dict = None) -> List[Base]:
    """Return some objects"""
    if not filters:
        filters = {}
    query = session.query(model)
    query = append_only.produce_append_only_query([model], query=query)
    compiled_filters = (getattr(model, param) == value for param, value in filters.items())
    query = query.filter(and_(*compiled_filters))
    result = query.all()
    return result


def insert(session: Session, model: Base, params: dict):
    """Insert one object"""
    m = model(**params)
    session.add(m)
    session.commit()
    session.refresh(m)
    return m


def update(session: Session, model: Base, filters: dict, params: dict):
    """Update one object"""
    rows = select(session, model, filters)
    obj_dict = _get_one_pure_dict(rows)
    updated = dict(params.items() - obj_dict.items())
    if updated:
        obj_dict.update(updated)
        return insert(session, model, obj_dict)
    else:
        return rows[0]


def delete(session: Session, model: Base, filters: dict):
    """Delete one object"""
    params = {"is_deleted": True}
    return update(session, model, filters, params)
