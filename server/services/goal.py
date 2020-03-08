from .service import Service, current_user_id, current_client_id
from models.goal_tree import GoalTree, GoalTreeNode
from models.note_category import NoteCategory
from utility import isTrue, isFalse, isNone, notNone

import datetime


class GoalService(Service):
    def __init__(self, session):
        super().__init__(session)

    def newTree(self, name):
        gtree = GoalTree(
            owner=current_client_id(),
            name=name,
            created_at=datetime.datetime.utcnow()
        )

        self._session.add(gtree)
        self._session.flush()

        beginning = self.newTreeNode(gtree.id, None, "Beginning")

        self._session.commit()
        return gtree

    def newTreeNode(self, tree, parent, title):
        node = GoalTreeNode(
            title=title,
            tree=tree,
            parent_node=parent,
            created_at=datetime.datetime.utcnow()
        )

        self._session.add(node)
        self._session.commit()
        return node

    def editTreeNode(self, tree, id, title, description):
        node = self.goalTreeNode(id)

        if node.tree != tree:
            raise RuntimeError("Node doesn't belong to tree")

        node.title = title
        node.description = description

        return node

    def goalTreeNode(self, id):
        return self._query(GoalTreeNode) \
                   .filter(GoalTreeNode.id == id) \
                   .first()

    def goalTreeList(self):
        return self._query(GoalTree) \
                   .filter(GoalTree.owner == current_client_id()) \
                   .filter(isNone(GoalTree.deleted_at)) \
                   .order_by(GoalTree.created_at.desc()) \
                   .all()

    def goalTreeFull(self, id):
        gtree = self._query(GoalTree) \
                   .filter(GoalTree.owner == current_client_id()) \
                   .filter(GoalTree.id == id) \
                   .first()
        nodes = self._query(GoalTreeNode) \
                   .filter(GoalTreeNode.tree == id) \
                   .filter(isNone(GoalTreeNode.deleted_at)) \
                   .order_by(GoalTreeNode.created_at.desc()) \
                   .all()
        gtree.nodes = nodes
        return gtree

    def moveNode(self, movedNodeId, targetNodeId):
        movedNode = self.goalTreeNode(movedNodeId)
        targetNode = self.goalTreeNode(targetNodeId)

        if movedNode.tree != targetNode.tree:
            raise RuntimeError("Trying to move to a different tree")

        parent = targetNode
        while parent.parent_node is not None:
            if parent.parent_node == movedNode.id:
                parent.parent_node = movedNode.parent_node
                break
            parent = self.goalTreeNode(parent.parent_node)

        movedNode.parent_node = targetNode.id

        return self.goalTreeFull(movedNode.tree)

    def deleteNode(self, treeId, nodeId):
        node = self.goalTreeNode(nodeId)

        if node.parent_node is None:
            raise RuntimeError("Trying to delete a root node")

        if node.tree != treeId:
            raise RuntimeError("Node doesn't belong to tree")

        node.deleted_at = datetime.datetime.utcnow()

        nodes = self._query(GoalTreeNode) \
                   .filter(GoalTreeNode.tree == treeId) \
                   .filter(isNone(GoalTreeNode.deleted_at)) \
                   .order_by(GoalTreeNode.created_at.desc()) \
                   .all()

        for n in nodes:
            print(n.deleted_at)
            if n.parent_node == node.id:
                n.parent_node = node.parent_node

        return self.goalTreeFull(treeId);
