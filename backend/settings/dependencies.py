import typing
from contextlib import contextmanager

from fastapi import Request
from sqlalchemy.orm import Session


def get_db(request: Request):
    return request.state.db

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
