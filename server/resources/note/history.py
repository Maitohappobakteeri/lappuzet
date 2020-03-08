from services.note import NoteService
from models.note import OwnNoteSchema
from db import with_session

from flask import request
from flask_restful import Resource, marshal_with
from flask_jwt_extended import jwt_required
from flasgger import swag_from


specs_dict = {
    "tags": ["Note"],

    "operationId": "loadHistory",

    "summary": "Gets resolved notes",

    "parameters": [
        {
            "in": "path",
            "name": "categoryId",
            "schema": { "type": "integer" },
            "required": "true",
            "description": "Note category"
        },
        {
            "in": "query",
            "name": "start",
            "schema": { "type": "integer" },
            "required": "true",
            "description": "Page start"
        },
        {
            "in": "query",
            "name": "amount",
            "schema": { "type": "integer" },
            "required": "true",
            "description": "Max notes returned"
        }
    ],

    "responses": {
        "200": {
            "description": "History",
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


class NoteHistoryResource(Resource):
    decorators = [jwt_required()]

    @swag_from(specs_dict)
    @with_session
    @marshal_with(OwnNoteSchema.marshaller())
    def get(self, session, categoryId):
        args = request.args
        notes = NoteService(session)
        return notes.history(categoryId, args["start"], args["amount"])
