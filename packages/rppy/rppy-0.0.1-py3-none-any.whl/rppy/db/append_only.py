# Give methods to work with append only db
# Maintain db columns: id, uid, created_at, is_deleted
from typing import List, Tuple

from sqlalchemy import and_
from sqlalchemy.orm import Query, aliased

from .base_class import Base


def base_append_only_query(model: Base, query: Query) -> Query:
    """
    This query is equal to
        SELECT tbl1.* FROM :tablename AS tbl1
        LEFT JOIN :tablename AS tbl2 ON
            tbl1.uid = tbl2.uid AND tbl2.id > tbl1.id
        WHERE
            tbl2.id IS NULL AND tbl1.is_deleted = false
    :return: SQLAlchemy Query
    """
    alias = aliased(model)
    query = query.outerjoin(alias, and_(alias.uid == model.uid, alias.id > model.id))
    query = query.filter(alias.id.is_(None))
    query = query.filter(model.is_deleted.is_(False))

    return query


def produce_append_only_query(models: List[Base], join_on_chain: List[Tuple[str, str]] = None,
                              query: Query = None) -> Query:
    if not query:
        query = Query([*models])

    for index, model in enumerate(models):
        if index > 0:
            # join with previous model in list
            left_name, right_name = join_on_chain[index - 1]
            prev_model = models[index - 1]

            query = query.outerjoin(
                model,
                getattr(prev_model, left_name) == getattr(model, right_name)
            )

        query = base_append_only_query(model, query)

    return query
