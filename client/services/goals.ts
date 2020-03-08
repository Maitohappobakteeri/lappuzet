import { environment } from "../environment";
import { map, filter } from "rxjs/operators";
import { Observable, forkJoin } from "rxjs";
import aes from "crypto-js/aes";
import CryptoJS from "crypto-js";
import { injectable, inject } from "inversify";
import { InjAccessProvider, IAccessProvider } from "./http-base";
import { InjSecretProvider, ISecretProvider } from "./isecret-provider";
import { ResultEither } from "./result-either";
import { NoteApi, GoalTreeApi } from "../generated-api/apis";
import { OwnNoteDto, NoteCategoryDto } from "../generated-api/models";

export type Note = {
  id: number;
  message: string;
  resolved: boolean;
  needsResolve: boolean;
  createdAt: Date;
};

@injectable()
export class GoalService {
  private goalApi: GoalTreeApi;

  constructor(
    @inject(InjAccessProvider) accessProvider: IAccessProvider,
    @inject(InjSecretProvider) private secretProvider: ISecretProvider
  ) {
    this.goalApi = new GoalTreeApi(accessProvider, environment.host);
  }

  loadList() {
    return this.goalApi.loadGoalTreeList();
  }

  loadFullTree(treeId: number) {
    return this.goalApi.loadGoalTree({ treeId });
  }

  createTree(name: string) {
    return this.goalApi.newGoalTree({ newGoalTreeDto: { name } });
  }

  createTreeNode(
    treeId: number,
    title: string,
    parent_node: number | undefined
  ) {
    return this.goalApi.newGoalTreeNode({
      treeId,
      newGoalTreeNodeDto: { title, parent_node }
    });
  }

  moveNode(treeId: number, movedNode: number, targetNode: number) {
    return this.goalApi.moveGoalTreeNode({ movedNode, targetNode });
  }

  editNode(treeId: number, nodeId: number, title: string, description: string) {
    return this.goalApi.editGoalTreeNode({
      treeId,
      nodeId,
      editGoalTreeNodeDto: { title, description }
    });
  }

  deleteNode(treeId: number, nodeId: number) {
    return this.goalApi.deleteGoalTreeNode({ treeId, nodeId });
  }
}
