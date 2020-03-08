from services.goal import GoalService
from models.goal_tree import GoalTreeFullSchema
from db import with_session

from flask import request
from flask_restful import Resource, marshal_with
from flask_jwt_extended import jwt_required
from flasgger import swag_from


specs_dict = {
    "tags": ["Goal Tree"],

    "operationId": "loadGoalTree",

    "summary": "Gets full goal tree",

    "parameters": [
        {
            "in": "path",
            "name": "treeId",
            "schema": { "type": "integer" },
            "required": "true"
        }
    ],

    "responses": {
        "200": {
            "description": "Goal tree",
            "content": {
                "application/json": {
                    "schema": GoalTreeFullSchema.schemaSpecRef()
                }
            }
        }
    }
}


class GoalTreeResource(Resource):
    decorators = [jwt_required()]

    @swag_from(specs_dict)
    @with_session
    @marshal_with(GoalTreeFullSchema.marshaller())
    def get(self, session, treeId):
        args = request.args
        goals = GoalService(session)
        return goals.goalTreeFull(treeId)
