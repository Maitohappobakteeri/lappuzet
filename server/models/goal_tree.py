from .base import Base
from .schema import Schema, Property, PropertyType

from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Boolean, CHAR
)
from flask_restful import fields


GoalTreeSchema = Schema(
    "GoalTree",
    [
        Property("id", PropertyType.integer),
        Property("name", PropertyType.string),
        Property("created_at", PropertyType.datetime),
    ]
)

NewGoalTreeSchema = Schema(
    "NewGoalTree",
    [
        Property("name", PropertyType.string),
    ]
)


class GoalTree(Base):
    __tablename__ = 'goal_tree'

    id = Column(Integer, primary_key=True)
    owner = Column(Integer, nullable=False)
    name = Column(String(64), nullable=False)
    created_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime)

GoalTreeNodeSchema = Schema(
    "GoalTreeNode",
    [
        Property("id", PropertyType.integer),
        Property("title", PropertyType.string),
        Property("description", PropertyType.string),
        Property("parent_node", PropertyType.integer, required=False),
    ]
)

GoalTreeFullSchema = Schema(
    "GoalTreeFull",
    [
        Property("id", PropertyType.integer),
        Property("name", PropertyType.string),
        Property("created_at", PropertyType.datetime),

        Property("nodes", PropertyType.array, items=GoalTreeNodeSchema),
    ]
)

NewGoalTreeNodeSchema = Schema(
    "NewGoalTreeNode",
    [
        Property("title", PropertyType.string),
        Property("description", PropertyType.string, required=False),
        Property("parent_node", PropertyType.integer, required=False),
    ]
)

EditGoalTreeNodeSchema = Schema(
    "EditGoalTreeNode",
    [
        Property("title", PropertyType.string),
        Property("description", PropertyType.string),
    ]
)


class GoalTreeNode(Base):
    __tablename__ = 'goal_tree_node'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    description = Column(String(512), nullable=False)
    created_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime)
    resolved_at = Column(DateTime)

    parent_node = Column(Integer, ForeignKey('goal_tree_node.id'))
    tree = Column(Integer, ForeignKey('goal_tree.id'), nullable=False)
