from services.note import NoteService
from models.note import OwnNoteSchema
from db import with_session

from flask_restful import Resource, marshal_with
from flask_jwt_extended import jwt_required
from flasgger import swag_from


specs_dict = {
    "tags": ["Note"],

    "operationId": "loadUnresolved",

    "parameters": [
        {
            "in": "path",
            "name": "categoryId",
            "schema": { "type": "integer" },
            "required": "true",
            "description": "Note category"
        }
    ],

    "summary": "Gets all unresolved notes",

    "responses": {
        "200": {
            "description": "Resolved note",
            "content": {
                "application/json": {
                    "schema": {
                      "type": "array",
                      "items": OwnNoteSchema.schemaSpecRef()
                    }
                }
            }
        }
    }
}


class NoteUnresolvedResource(Resource):
    decorators = [jwt_required()]

    @swag_from(specs_dict)
    @with_session
    @marshal_with(OwnNoteSchema.marshaller())
    def get(self, session, categoryId):
        notes = NoteService(session)
        return notes.unresolved(categoryId)
