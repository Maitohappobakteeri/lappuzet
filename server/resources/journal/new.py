from services.journal import JournalService
from models.note import OwnJournalNoteSchema, NewJournalNoteSchema
from db import with_session

from flask_restful import Resource, marshal_with, reqparse
from flask_jwt_extended import jwt_required
from flasgger import swag_from


specs_dict = {
    "tags": ["Journal"],

    "operationId": "newNote",

    "summary": "Creates a new journal note",

    "requestBody": {
        "description": "the **new** note",
        "required": "true",
        "content": {
            "application/json": {
                "schema": NewJournalNoteSchema.schemaSpecRef()
            }
        }
    },

    "responses": {
        "200": {
            "description": "Created note",
            "content": {
                "application/json": {
                    "schema": OwnJournalNoteSchema.schemaSpecRef()
                }
            }
        }
    }
}


_parser = reqparse.RequestParser()
_parser.add_argument('message', type=str)
_parser.add_argument('food', type=int)
_parser.add_argument('mood', type=str)
_parser.add_argument('stress', type=str)
_parser.add_argument('sleep', type=str)


class JournalNewResource(Resource):
    decorators = [jwt_required()]

    @swag_from(specs_dict)
    @with_session
    @marshal_with(OwnJournalNoteSchema.marshaller())
    def post(self, session):
        args = _parser.parse_args()
        journal = JournalService(session)
        return journal.new(args.message, {
            "food": args.food,
            "sleep": args.sleep,
            "mood": args.mood,
            "stress": args.stress,
        })
