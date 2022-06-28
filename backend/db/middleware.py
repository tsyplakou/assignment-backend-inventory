from threading import local

from .base import Session


class SessionRegistry(local):
    session = None

registry = SessionRegistry()

class Middleware:

    def on_request_start(self, request):
        registry.session = Session()

    def on_request_error(self, request):
        registry.session.close()
        registry.session = None

    def on_response(self, response):
        registry.session.commit()
        registry.session.close()
        registry.session = None
