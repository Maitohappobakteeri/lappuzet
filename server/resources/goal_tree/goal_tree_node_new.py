from services.goal import GoalService
from models.goal_tree import NewGoalTreeNodeSchema, GoalTreeNodeSchema
from db import with_session

from flask_restful import Resource, marshal_with, reqparse
from flask_jwt_extended import jwt_required
from flasgger import swag_from


specs_dict = {
    "tags": ["Goal Tree"],

    "operationId": "newGoalTreeNode",

    "summary": "Creates a new node",

    "parameters": [
        {
            "in": "path",
            "name": "treeId",
            "schema": { "type": "integer" },
            "required": "true"
        }
    ],

    "requestBody": {
        "description": "the **new** node",
        "required": "true",
        "title": "newGoalTreeNodeDto",
        "content": {
            "application/json": {
                "schema": NewGoalTreeNodeSchema.schemaSpecRef()
            }
        }
    },

    "responses": {
        "200": {
            "description": "Created node",
            "content": {
                "application/json": {
                    "schema": GoalTreeNodeSchema.schemaSpecRef()
                }
            }
        }
    }
}


_parser = reqparse.RequestParser()
_parser.add_argument('parent_node', type=int)
_parser.add_argument('title', type=str)


class GoalTreeNodeNewResource(Resource):
    decorators = [jwt_required()]

    @swag_from(specs_dict)
    @with_session
    @marshal_with(GoalTreeNodeSchema.marshaller())
    def post(self, session, treeId):
        args = _parser.parse_args()
        goal = GoalService(session)
        return goal.newTreeNode(treeId, args.parent_node, args.title)
