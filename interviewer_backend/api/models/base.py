from __future__ import annotations

import asyncio
import re
from contextlib import asynccontextmanager
from typing import AsyncIterator

import sqlalchemy
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Query, Session, as_declarative, declared_attr

from api.exceptions import APIError, ObjectNotFound


@as_declarative()
class Base:
    """Base class for all database entities"""

    @declared_attr
    def __tablename__(cls) -> str:  # pylint: disable=no-self-argument
        """Generate database table name automatically.
        Convert CamelCase class name to snake_case db table name.
        """
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()

    def __repr__(self):
        attrs = []
        for c in self.__table__.columns:
            attrs.append(f"{c.name}={getattr(self, c.name)}")
        return "{}({})".format(c.__class__.__name__, ', '.join(attrs))


class BaseDbModel(Base):
    __abstract__ = True

    @classmethod
    def create(cls, *, session: Session, **kwargs) -> BaseDbModel:
        obj = cls(**kwargs)
        session.add(obj)
        session.flush()
        return obj

    @classmethod
    def query(cls, *, session: Session) -> Query:
        objs = session.query(cls)
        return objs

    @classmethod
    def get(cls, id: int | str, *, session: Session) -> BaseDbModel:
        objs = session.query(cls)
        try:
            return objs.filter(cls.id == id).one()
        except NoResultFound:
            raise ObjectNotFound(cls, id)

    @classmethod
    def update(cls, id: int | str, *, session: Session, **kwargs) -> BaseDbModel:
        obj = cls.get(id, session=session)
        for k, v in kwargs.items():
            setattr(obj, k, v)
        session.flush()
        return obj

    @classmethod
    def delete(cls, id: int | str, *, session: Session) -> None:
        obj = cls.get(id, session=session)
        session.delete(obj)
        session.flush()

    @classmethod
    @asynccontextmanager
    async def lock(cls, session: Session) -> AsyncIterator[Session]:
        """
        First, we try to capture the table lock.

        Since we are using synchronous alchemy, we will create a timeout and will not wait for it anymore.

        If the lock is held by another coroutine, then eventually we will exit the timeout and block the coroutine with asynchronous sleep.

        Thus, we will let the coroutine holding the lock finish its work.
        """
        for _ in range(3):
            nested = session.begin_nested()
            session.execute(sqlalchemy.text("SET LOCAL lock_timeout = '0.2s';"))
            try:
                session.execute(sqlalchemy.text(f'LOCK TABLE "{cls.__tablename__}" IN ACCESS EXCLUSIVE MODE;'))
            except sqlalchemy.exc.OperationalError:
                nested.rollback()
                await asyncio.sleep(1.5)
            else:
                break
        else:
            raise APIError("Internal Server Error")
        try:
            yield session
        except Exception:
            nested.rollback()
            session.rollback()
            if session and session.is_active:
                session.close()
            raise
        else:
            nested.commit()
            session.commit()
            if session and session.is_active:
                session.close()
