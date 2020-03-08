from services.goal import GoalService
from models.goal_tree import NewGoalTreeSchema, GoalTreeSchema
from db import with_session

from flask_restful import Resource, marshal_with, reqparse
from flask_jwt_extended import jwt_required
from flasgger import swag_from


specs_dict = {
    "tags": ["Goal Tree"],

    "operationId": "newGoalTree",

    "summary": "Creates a new goal tree",

    "requestBody": {
        "description": "the **new** goal tree",
        "required": "true",
        "title": "newGoalTreeDto",
        "content": {
            "application/json": {
                "schema": NewGoalTreeSchema.schemaSpecRef()
            }
        }
    },

    "responses": {
        "200": {
            "description": "Created goal tree",
            "content": {
                "application/json": {
                    "schema": GoalTreeSchema.schemaSpecRef()
                }
            }
        }
    }
}


_parser = reqparse.RequestParser()
_parser.add_argument('name', type=str)


class GoalTreeNewResource(Resource):
    decorators = [jwt_required()]

    @swag_from(specs_dict)
    @with_session
    @marshal_with(GoalTreeSchema.marshaller())
    def post(self, session):
        args = _parser.parse_args()
        goal = GoalService(session)
        return goal.newTree(args.name)
