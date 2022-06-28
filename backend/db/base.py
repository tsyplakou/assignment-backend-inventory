import os
import typing
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine(os.environ['DB_URL'], echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class_registry: typing.Dict = {}


@as_declarative(class_registry=class_registry)
class Base:
    id: typing.Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


@contextmanager
def session(**kwargs) -> typing.ContextManager[Session]:
    new_session = Session(**kwargs)
    try:
        yield new_session
        new_session.commit()
    except Exception as e:
        new_session.rollback()
        raise e
    finally:
        new_session.close()
