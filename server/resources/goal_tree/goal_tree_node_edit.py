from services.goal import GoalService
from models.goal_tree import EditGoalTreeNodeSchema, GoalTreeNodeSchema
from db import with_session

from flask_restful import Resource, marshal_with, reqparse
from flask_jwt_extended import jwt_required
from flasgger import swag_from


specs_dict = {
    "tags": ["Goal Tree"],

    "operationId": "editGoalTreeNode",

    "summary": "Edits a node",

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

    "requestBody": {
        "description": "the **edited** node",
        "required": "true",
        "content": {
            "application/json": {
                "schema": EditGoalTreeNodeSchema.schemaSpecRef()
            }
        }
    },

    "responses": {
        "200": {
            "description": "Edited node",
            "content": {
                "application/json": {
                    "schema": GoalTreeNodeSchema.schemaSpecRef()
                }
            }
        }
    }
}


_parser = reqparse.RequestParser()
_parser.add_argument('title', type=str)
_parser.add_argument('description', type=str)


class GoalTreeNodeEditResource(Resource):
    decorators = [jwt_required()]

    @swag_from(specs_dict)
    @with_session
    @marshal_with(GoalTreeNodeSchema.marshaller())
    def put(self, session, treeId, nodeId):
        args = _parser.parse_args()
        goal = GoalService(session)
        return goal.editTreeNode(int(treeId), int(nodeId), args.title, args.description)
