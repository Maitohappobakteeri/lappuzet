from services.goal import GoalService
from models.goal_tree import GoalTreeFullSchema
from db import with_session

from flask_restful import Resource, marshal_with, reqparse
from flask_jwt_extended import jwt_required
from flasgger import swag_from


specs_dict = {
    "tags": ["Goal Tree"],

    "operationId": "moveGoalTreeNode",

    "summary": "Moves goal tree node to target position",

    "parameters": [
        {
            "in": "path",
            "name": "movedNode",
            "schema": { "type": "integer" },
            "required": "true"
        },
        {
            "in": "path",
            "name": "targetNode",
            "schema": { "type": "integer" },
            "required": "true"
        },
    ],

    "responses": {
        "200": {
            "description": "Edited goal tree",
            "content": {
                "application/json": {
                    "schema": GoalTreeFullSchema.schemaSpecRef()
                }
            }
        }
    }
}


class GoalTreeMoveNodeResource(Resource):
    decorators = [jwt_required()]

    @swag_from(specs_dict)
    @with_session
    @marshal_with(GoalTreeFullSchema.marshaller())
    def put(self, session, movedNode, targetNode):
        goal = GoalService(session)
        return goal.moveNode(movedNode, targetNode)
