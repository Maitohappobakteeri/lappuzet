from services.user import UserService
from services.note import NoteService
from services.goal import GoalService
from services.journal import JournalService
from models.user import UserSchema
from db import with_session

from flask_restful import Resource, marshal_with
from flask_jwt_extended import jwt_required
from flasgger import swag_from


specs_dict = {
    "tags": ["User"],

    "summary": "Gets current user",

    "responses": {
        "200": {
            "description": "Current user",
            "content": {
                "application/json": {
                    "schema": UserSchema.schemaSpecRef()
                }
            }
        }
    }
}


class UserResource(Resource):
    decorators = [jwt_required()]

    @swag_from(specs_dict)
    @with_session
    @marshal_with(UserSchema.marshaller())
    def get(self, session):
        userService = UserService(session)

        notes = NoteService(session)

        if len(notes.categoryList()) == 0:
            category = notes.newCategory("Tärkeet")     
            goal = GoalService(session)
            root = goal.newTree("Ekat tavoitteet")

        return userService.current()
