from services.note import NoteService
from models.note_category import NoteCategorySchema, NewNoteCategorySchema
from db import with_session

from flask_restful import Resource, marshal_with, reqparse
from flask_jwt_extended import jwt_required
from flasgger import swag_from


specs_dict = {
    "tags": ["Note"],

    "operationId": "newCategory",

    "summary": "Creates a new note category",

    "requestBody": {
        "description": "the **new** note category",
        "required": "true",
        "title": "newNoteDto",
        "content": {
            "application/json": {
                "schema": NewNoteCategorySchema.schemaSpecRef()
            }
        }
    },

    "responses": {
        "200": {
            "description": "Created note category",
            "content": {
                "application/json": {
                    "schema": NoteCategorySchema.schemaSpecRef()
                }
            }
        }
    }
}


_parser = reqparse.RequestParser()
_parser.add_argument('name', type=str)


class NoteCategoryNewResource(Resource):
    decorators = [jwt_required()]

    @swag_from(specs_dict)
    @with_session
    @marshal_with(NoteCategorySchema.marshaller())
    def post(self, session):
        args = _parser.parse_args()
        notes = NoteService(session)
        return notes.newCategory(args.name)
