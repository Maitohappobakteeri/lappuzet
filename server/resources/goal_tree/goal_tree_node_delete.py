from services.goal import GoalService
from models.goal_tree import GoalTreeFullSchema
from db import with_session

from flask_restful import Resource, marshal_with, reqparse
from flask_jwt_extended import jwt_required
from flasgger import swag_from


specs_dict = {
    "tags": ["Goal Tree"],

    "operationId": "deleteGoalTreeNode",

    "summary": "Deletes a node",

    "parameters": [
        {
            "in": "path",
            "name": "treeId",
            "schema": { "type": "integer" },
            "required": "true"
        },
        {
            "in": "path",
            "name": "nodeId",
            "schema": { "type": "integer" },
            "required": "true"
        }
    ],

    "responses": {
        "200": {
            "description": "Modified goal tree",
            "content": {
                "application/json": {
                    "schema": GoalTreeFullSchema.schemaSpecRef()
                }
            }
        }
    }
}


class GoalTreeNodeDeleteResource(Resource):
    decorators = [jwt_required()]

    @swag_from(specs_dict)
    @with_session
    @marshal_with(GoalTreeFullSchema.marshaller())
    def delete(self, session, treeId, nodeId):
        goal = GoalService(session)
        return goal.deleteNode(int(treeId), int(nodeId))
