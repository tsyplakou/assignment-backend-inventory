import typing
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

engine = create_engine('sqlite:///:memory:', echo=True) # os.environ['DB_URL']
Base = declarative_base()

Session = sessionmaker()
current_session = scoped_session(Session) # thread local variable


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
