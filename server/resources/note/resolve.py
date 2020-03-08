from services.note import NoteService
from models.note import OwnNoteSchema
from db import with_session

from flask_restful import Resource, marshal_with
from flask_jwt_extended import jwt_required
from flasgger import swag_from


specs_dict = {
    "tags": ["Note"],

    "operationId": "resolveNote",

    "summary": "Resolve note",

    "parameters": [
        {
            "in": "path",
            "name": "noteId",
            "schema": { "type": "integer" },
            "required": "true",
            "description": "Note to be resolved"
        },
    ],

    "responses": {
        "200": {
            "description": "Resolved note",
            "content": {
                "application/json": {
                    "schema": OwnNoteSchema.schemaSpecRef()
                }
            }
        }
    }
}


class NoteResolveResource(Resource):
    decorators = [jwt_required()]

    @swag_from(specs_dict)
    @with_session
    @marshal_with(OwnNoteSchema.marshaller())
    def put(self, session, noteId):
        notes = NoteService(session)
        return notes.resolve(noteId)
