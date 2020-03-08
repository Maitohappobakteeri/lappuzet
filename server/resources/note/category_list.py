from services.note import NoteService
from models.note_category import NoteCategorySchema
from db import with_session

from flask import request
from flask_restful import Resource, marshal_with
from flask_jwt_extended import jwt_required
from flasgger import swag_from


specs_dict = {
    "tags": ["Note"],

    "operationId": "loadCategories",

    "summary": "Gets note categories",

    "responses": {
        "200": {
            "description": "Categories",
            "content": {
                "application/json": {
                    "schema": {
                      "type": "array",
                      "items": NoteCategorySchema.schemaSpecRef()
                    }
                }
            }
        }
    }
}


class NoteCategoryListResource(Resource):
    decorators = [jwt_required()]

    @swag_from(specs_dict)
    @with_session
    @marshal_with(NoteCategorySchema.marshaller())
    def get(self, session):
        args = request.args
        notes = NoteService(session)
        return notes.categoryList()
