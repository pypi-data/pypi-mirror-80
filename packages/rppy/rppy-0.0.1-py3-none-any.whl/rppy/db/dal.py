from . import crud
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from typing import TypeVar
import uuid

DataObj = TypeVar('DataObj')
DBDataObj = TypeVar('DBDataObj')


class BaseDal(object):
    def __init__(self, session, model, validation_schema):
        self._session = session
        self._model = model
        self.validation_schema = validation_schema

    def _select(self, filters=None):
        result = crud.select(self._session, self._model, filters)
        return result

    def _create(self, params):
        result = crud.insert(self._session, self._model, params)
        return result

    def _update(self, filters, params):
        result = crud.update(self._session, self._model, filters, params)
        return result

    def _delete(self, filters):
        result = crud.delete(self._session, self._model, filters)
        return result

    def _get_or_create(self, filters, params):
        """Check model existing, and if not - create it"""
        obj = self.one_or_none(filters)
        if obj:
            return obj
        else:
            return self.create(params)

    def _update_or_create(self, filters, params):
        obj = self.one_or_none(filters)
        if obj:
            return self.update(filters, params)
        else:
            return self.create(params)

    def _one_or_none(self, filters):
        """Return one or None objects"""
        result = crud.select(self._session, self._model, filters)
        if len(result) == 0:
            return None
        if len(result) > 1:
            raise MultipleResultsFound
        return result[0]

    def _one(self, filters):
        """If not exactly one result raised exception"""
        result = crud.select(self._session, self._model, filters)
        if len(result) < 1:
            raise NoResultFound
        if len(result) > 1:
            raise MultipleResultsFound
        obj = result[0]
        return obj

    def get_all(self, filters: dict = None):
        result = self._select(filters)
        return result

    def get(self, uid: uuid.UUID) -> DBDataObj:
        filters = {"uid": uid}
        obj = self.one(filters)
        return self.validation_schema.from_orm(obj)

    def create(self, data_obj: DataObj) -> DBDataObj:
        params = data_obj.dict(skip_defaults=True)
        created_obj = self._create(params)
        return self.validation_schema.from_orm(created_obj)

    def update(self, uid: uuid.UUID, data_obj: DataObj) -> DBDataObj:
        filters = {"uid": uid}
        params = {k: v for k, v in data_obj.dict(skip_defaults=True).items() if v is not None}
        updated_obj = self._update(filters, params)
        return self.validation_schema.from_orm(updated_obj)

    def delete(self, uid: uuid.UUID) -> DBDataObj:
        filters = {"uid": uid}
        deleted_obj = self._delete(filters)
        return self.validation_schema.from_orm(deleted_obj)

    def get_or_create(self, filters, params) -> DBDataObj:
        """Check model existing, and if not - create it"""
        obj = self._get_or_create(filters, params)
        return self.validation_schema.from_orm(obj)

    def update_or_create(self, filters, params) -> DBDataObj:
        obj = self._update_or_create(filters, params)
        return self.validation_schema.from_orm(obj)

    def one_or_none(self, filters) -> DBDataObj:
        """Return one or None objects"""
        obj = self._one_or_none(filters)
        if obj:
            return self.validation_schema.from_orm(obj)
        else:
            return None

    def one(self, filters) -> DBDataObj:
        """If not exactly one result raised exception"""
        obj = self._one(filters)
        return self.validation_schema.from_orm(obj)
