from services.auth import AuthService
from db import with_session

from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
)


class RefreshResource(Resource):
    decorators = [jwt_required(refresh=True)]

    @with_session
    def post(self, session):
        authService = AuthService(session)
        return authService.refresh()
