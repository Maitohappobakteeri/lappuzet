from services.note import NoteService
from models.note import OwnNoteSchema, NewNoteSchema
from db import with_session

from flask_restful import Resource, marshal_with, reqparse
from flask_jwt_extended import jwt_required
from flasgger import swag_from


specs_dict = {
    "tags": ["Note"],

    "operationId": "newNote",

    "summary": "Creates a new note",

    "parameters": [
        {
            "in": "path",
            "name": "categoryId",
            "schema": { "type": "integer" },
            "required": "true",
            "description": "Note category"
        }
    ],

    "requestBody": {
        "description": "the **new** note",
        "required": "true",
        "title": "newNoteDto",
        "content": {
            "application/json": {
                "schema": NewNoteSchema.schemaSpecRef()
            }
        }
    },

    "responses": {
        "200": {
            "description": "Created note",
            "content": {
                "application/json": {
                    "schema": OwnNoteSchema.schemaSpecRef()
                }
            }
        }
    }
}


_parser = reqparse.RequestParser()
_parser.add_argument('message', type=str)
_parser.add_argument('needsResolve', type=bool)
_parser.add_argument('category', type=int)


class NoteNewResource(Resource):
    decorators = [jwt_required()]

    @swag_from(specs_dict)
    @with_session
    @marshal_with(OwnNoteSchema.marshaller())
    def post(self, session, categoryId):
        args = _parser.parse_args()
        notes = NoteService(session)
        return notes.new(categoryId, args.message, args.needsResolve)
