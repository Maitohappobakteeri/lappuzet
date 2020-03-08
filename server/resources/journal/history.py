from services.journal import JournalService
from models.note import OwnJournalNoteSchema
from db import with_session

from flask import request
from flask_restful import Resource, marshal_with
from flask_jwt_extended import jwt_required
from flasgger import swag_from


specs_dict = {
    "tags": ["Journal"],

    "operationId": "loadHistory",

    "summary": "Gets journal notes",

    "parameters": [
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
            "description": "Journal notes",
            "content": {
                "application/json": {
                    "schema": {
                      "type": "array",
                      "items": OwnJournalNoteSchema.schemaSpecRef()
                    }
                }
            }
        }
    }
}


class JournalHistoryResource(Resource):
    decorators = [jwt_required()]

    @swag_from(specs_dict)
    @with_session
    @marshal_with(OwnJournalNoteSchema.marshaller())
    def get(self, session):
        args = request.args
        journal = JournalService(session)
        return journal.history(args["start"], args["amount"])
