#!flask/bin/python

import environment
from db import with_session2

from flask import Flask, jsonify, request
from flask_restful import abort, Api
from flask_jwt_extended import (
    JWTManager, verify_jwt_in_request
)

from flasgger import Swagger
import flask_restful

import datetime

from services.auth import AuthService


from resources.user.user import UserResource

from resources.note.new import NoteNewResource
from resources.note.resolve import NoteResolveResource
from resources.note.unresolved import NoteUnresolvedResource
from resources.note.history import NoteHistoryResource
from resources.note.category_list import NoteCategoryListResource
from resources.note.category_new import NoteCategoryNewResource

from resources.auth.refresh import RefreshResource
from resources.auth.logout import LogoutResource

from resources.journal.new import JournalNewResource
from resources.journal.history import JournalHistoryResource

from resources.goal_tree.goal_tree_list import GoalTreeListResource
from resources.goal_tree.goal_tree import GoalTreeResource
from resources.goal_tree.goal_tree_new import GoalTreeNewResource
from resources.goal_tree.goal_tree_node_new import GoalTreeNodeNewResource
from resources.goal_tree.goal_tree_move_node import GoalTreeMoveNodeResource
from resources.goal_tree.goal_tree_node_delete import GoalTreeNodeDeleteResource
from resources.goal_tree.goal_tree_node_edit import GoalTreeNodeEditResource

from models.schema import openapiSchemas

from collections import OrderedDict


def marshal(data, fields, envelope=None):
    def make(cls):
        if isinstance(cls, type):
            return cls()
        return cls

    if isinstance(data, (list, tuple)):
        return (OrderedDict([(envelope, [marshal(d, fields) for d in data])])
                if envelope else [marshal(d, fields) for d in data])

    items = ((k, marshal(data, v) if isinstance(v, dict)
              else make(v).output(k, data))
             for k, v in fields.items())
    #filtering None
    items = ((k,v) for k, v in items if v is not None)
    return OrderedDict([(envelope, OrderedDict(items))]) if envelope else OrderedDict(items)

flask_restful.marshal = marshal

app = Flask(__name__)
app.config['SECRET_KEY'] = environment.Secret
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=5)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=7)
app.config['SWAGGER'] = {"openapi": "3.0.3"}
app.config['PROPAGATE_EXCEPTIONS'] = True

swagger_config = {
    "headers": [],
    "servers": [
        {
            "url": "http://127.0.0.1:5000/",
            "description": "Local"
        }
    ],
    "specs": [
        {
            "endpoint": "swagger",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "title": "Lappuzet",
    "version": '0.0.1',
    "termsOfService": "",
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "description": "",
}

jwt = JWTManager(app)
swagger = Swagger(app, config=swagger_config, template={
    "components": {
        "schemas": openapiSchemas,
    },
    "definitions": openapiSchemas
    }
)

if environment.useCors:
    from flask_cors import CORS
    CORS(app)

api = Api(app)
api.add_resource(UserResource, '/user')
api.add_resource(NoteNewResource, '/notes/category/<categoryId>/new')
api.add_resource(NoteResolveResource, '/notes/<noteId>/resolve')
api.add_resource(NoteUnresolvedResource, '/notes/category/<categoryId>/unresolved')
api.add_resource(NoteHistoryResource, '/notes/category/<categoryId>/history')

api.add_resource(NoteCategoryListResource, '/notes/category')
api.add_resource(NoteCategoryNewResource, '/notes/category/new')

api.add_resource(RefreshResource, '/refresh')
api.add_resource(LogoutResource, '/logout')
api.add_resource(JournalNewResource, '/journal/category/new')
api.add_resource(JournalHistoryResource, '/journal/category/history')

api.add_resource(GoalTreeListResource, '/goaltree')
api.add_resource(GoalTreeResource, '/goaltree/<treeId>')
api.add_resource(GoalTreeNewResource, '/goaltree/new')
api.add_resource(GoalTreeNodeNewResource, '/goaltree/<treeId>/node/new')
api.add_resource(GoalTreeMoveNodeResource, '/goaltree/nodes/<movedNode>/move/<targetNode>')
api.add_resource(GoalTreeNodeDeleteResource, '/goaltree/<treeId>/node/<nodeId>')
api.add_resource(GoalTreeNodeEditResource, '/goaltree/<treeId>/node/<nodeId>')

@jwt.token_in_blocklist_loader
@with_session2
def check_if_token_not_in_use(session, somethinglol, decrypted_token):
    print(decrypted_token)
    jti = decrypted_token['jti']
    authService = AuthService(session)
    usersTokens = authService.tokens(decrypted_token["sub"])
    return jti not in (token.jti for token in usersTokens)


@app.route('/version', methods=['GET'])
def version():
    return jsonify({"app": "lappuzet"}), 200


@app.route('/login', methods=['POST'])
@with_session2
def login(session):
    authService = AuthService(session)
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    client = request.json.get('client', None)
    tokens = authService.login(username, password, client)
    if tokens:
        return jsonify(tokens), 200
    return jsonify({"msg": "Unauthorized"}), 401


@app.route('/')
def index():
    abort(404)


if __name__ == '__main__':
    app.run(debug=True)
