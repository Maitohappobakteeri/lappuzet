from services.goal import GoalService
from models.goal_tree import GoalTreeSchema
from db import with_session

from flask import request
from flask_restful import Resource, marshal_with
from flask_jwt_extended import jwt_required
from flasgger import swag_from


specs_dict = {
    "tags": ["Goal Tree"],

    "operationId": "loadGoalTreeList",

    "summary": "Gets goal tree",

    "responses": {
        "200": {
            "description": "Goal tree list",
            "content": {
                "application/json": {
                    "schema": {
                      "type": "array",
                      "items": GoalTreeSchema.schemaSpecRef()
                    }
                }
            }
        }
    }
}


class GoalTreeListResource(Resource):
    decorators = [jwt_required()]

    @swag_from(specs_dict)
    @with_session
    @marshal_with(GoalTreeSchema.marshaller())
    def get(self, session):
        args = request.args
        goals = GoalService(session)
        return goals.goalTreeList()
