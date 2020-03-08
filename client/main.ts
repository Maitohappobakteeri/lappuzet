import Vue from "vue";
import Vuex, { ActionContext } from "vuex";
import VueRouter from "vue-router";
import Buefy from "buefy";
import "babel-polyfill";
import app from "./ui/app.vue";
import notesComponent from "./ui/notes.vue";
import journalComponent from "./ui/journal/journal.vue";
import goalComponent from "./ui/goals.vue";
import { Auth } from "./services/auth";
import { flatMap, filter } from "rxjs/operators";
import { User, UserService } from "./services/user";
import { NoteService, Note } from "./services/notes";
import { notNull, isNull } from "./utility/observables";
import { AppStorage } from "./services/storage";
import { JournalService, JournalEntry } from "./services/journal";
import { Container } from "inversify";
import { InjAccessProvider } from "./services/http-base";
import { InjSecretProvider } from "./services/isecret-provider";
import {
  NoteCategoryDto,
  GoalTreeDto,
  GoalTreeFullDto,
  GoalTreeNodeDto
} from "./generated-api";
import { GoalService } from "./services/goals";
import { isDefined } from "./utility/type-guards";

Vue.use(Vuex);
Vue.use(VueRouter);
Vue.use(Buefy);

const routes = [
  { path: "/notes", component: notesComponent },
  { path: "/journal", component: journalComponent, name: "journal" },
  { path: "/goals", component: goalComponent, name: "goal" },
  { path: "/", redirect: "/notes" }
];

const router = new VueRouter({
  routes
});

type State = {
  login: { error: boolean; pending: boolean };
  user: User | null;

  categories: NoteCategoryDto[];
  currentCategory?: number;

  goalTrees: GoalTreeDto[];
  currentGoalTree?: number;
  fullGoalTree?: GoalTreeFullDto;

  notes: Note[];
  notesLoading: boolean;
  journal: JournalEntry[];
  journalLoading: boolean;
  uploadingData: boolean;
};

const container = new Container({ skipBaseClassChecks: true });

container
  .bind(AppStorage)
  .toSelf()
  .inSingletonScope();

container
  .bind(Auth)
  .toSelf()
  .inSingletonScope();

const auth = container.get(Auth);
container.bind(InjAccessProvider).toConstantValue(auth);
container.bind(InjSecretProvider).toConstantValue(auth);
container.bind(UserService).toSelf();
container.bind(NoteService).toSelf();
container.bind(GoalService).toSelf();
container.bind(JournalService).toSelf();

const storage = container.get(AppStorage);
const users = container.get(UserService);
const notes = container.get(NoteService);
const goals = container.get(GoalService);
const journal = container.get(JournalService);

export interface Mutations {
  signin: { username: string; password: string };
  signOut: undefined;
  signedIn: User;
  signedOut: undefined;
  authPending: undefined;
  startLoadingNotes: undefined;
  setNotes: Note[];
  startLoadingJournal: undefined;
  setJournal: JournalEntry[];
  addNote: Note;
  addJournalEntry: JournalEntry;
  updateNote: Note;
  startUploadingData: undefined;
  finishUploadingData: undefined;

  setCategories: NoteCategoryDto[];
  setCurrentCategory: number;
  addCategory: NoteCategoryDto;

  setGoalTrees: GoalTreeDto[];
  setCurrentGoalTree: number;
  addGoalTree: GoalTreeDto;
  setFullGoalTree: GoalTreeFullDto;
  addNewGoalTreeNode: GoalTreeNodeDto;
  editGoalTreeNode: GoalTreeNodeDto;
}

const mutations: {
  [K in keyof Mutations]: (state: State, payload: Mutations[K]) => void;
} = {
  signin(state, args: { username: string; password: string }) {
    state.login = { error: false, pending: true };
    auth.login(args.username, args.password);
  },
  signOut() {
    auth.logout();
  },
  signedIn(state, user) {
    state.user = user;
  },
  signedOut(state) {
    state.user = null;
    state.login = { error: true, pending: false };
  },
  authPending(state) {
    state.login = { error: false, pending: true };
  },
  startLoadingNotes(state) {
    state.notesLoading = true;
  },
  setNotes(state, notes: Note[]) {
    state.notesLoading = false;
    state.notes = notes.sort((a, b) =>
      b.resolved == a.resolved
        ? b.createdAt.getTime() - a.createdAt.getTime()
        : b.resolved
        ? -1
        : 1
    );
  },
  startLoadingJournal(state) {
    state.journalLoading = true;
  },
  setJournal(state, entries: JournalEntry[]) {
    state.journalLoading = false;
    state.journal = entries.sort(
      (a, b) => b.createdAt.getTime() - a.createdAt.getTime()
    );
  },
  addNote(state, note) {
    state.notes.unshift(note);
  },
  addJournalEntry(state, entry) {
    state.journal.unshift(entry);
  },
  updateNote(state, note: Note) {
    Vue.set(
      state.notes,
      state.notes.findIndex(n => n.id === note.id),
      note
    );
  },
  startUploadingData(state) {
    state.uploadingData = true;
  },
  finishUploadingData(state) {
    // TODO: Never gets set if fetch fails on network error
    //       I think the observable gets never made in that case
    //       -> from fails -> complete never runs
    state.uploadingData = false;
  },

  setCategories(state, categories: NoteCategoryDto[]) {
    state.categories = categories;
    if (state.currentCategory == undefined) {
      state.currentCategory = state.categories[0]?.id;
    }
  },
  setCurrentCategory(state, category: number) {
    state.currentCategory = category;
    storage.state.notes.selectedCategory = category;
    storage.update();
  },
  addCategory(state, category: NoteCategoryDto) {
    state.categories.push(category);
  },

  setGoalTrees(state, trees: GoalTreeDto[]) {
    state.goalTrees = trees;
    if (state.currentGoalTree == undefined) {
      state.currentGoalTree = state.goalTrees[0]?.id;
    }
  },
  setCurrentGoalTree(state, tree: number) {
    state.currentGoalTree = tree;
    storage.state.goals.selectedTree = tree;
    storage.update();
  },
  addGoalTree(state, tree: GoalTreeDto) {
    state.goalTrees.push(tree);
  },
  setFullGoalTree(state, tree: GoalTreeFullDto) {
    state.fullGoalTree = tree;
  },
  addNewGoalTreeNode(state, newNode: GoalTreeNodeDto) {
    if (state.fullGoalTree) {
      state.fullGoalTree.nodes.push(newNode);
    }
  },
  editGoalTreeNode(state, node: GoalTreeNodeDto) {
    const gtree = state.fullGoalTree;
    if (isDefined(gtree)) {
      Vue.set(
        gtree.nodes,
        gtree.nodes.findIndex(n => n.id === node.id),
        node
      );
    }
  }
};

type OptionalSpread<T = undefined> = T extends undefined ? [] : [T];

class ContextWrapper<M> {
  constructor(private context: ActionContext<State, State>) {}

  commit<K extends keyof M & string>(
    type: K,
    ...payload: OptionalSpread<M[K]>
  ) {
    this.context.commit(type, ...payload);
  }
}

function wrap(context: ActionContext<State, State>) {
  return new ContextWrapper<Mutations>(context);
}

const store = new Vuex.Store<State>({
  state: {
    login: {
      error: false,
      pending: false
    },
    user: null,
    notes: [],
    notesLoading: false,
    journal: [],
    journalLoading: false,
    uploadingData: false,

    categories: [],
    currentCategory: storage.state.notes.selectedCategory,

    goalTrees: [],
    currentGoalTree: storage.state.goals.selectedTree,
    fullGoalTree: undefined
  },
  mutations,
  getters: {
    currentCategory(state) {
      return state.categories.find(c => c.id == state.currentCategory);
    },
    currentGoalTree(state) {
      return state.fullGoalTree?.id == state.currentGoalTree
        ? state.fullGoalTree
        : state.goalTrees.find(c => c.id == state.currentGoalTree);
    },
    journalStats(state) {
      const j = [...state.journal];
      j.reverse();
      return [
        {
          label: "Mood",
          data: j.map(j => j.mood),
          fill: false,
          borderColor: "red",
          tension: 0.1
        },
        {
          label: "Sleep",
          data: j.map(j => j.sleep),
          fill: false,
          borderColor: "blue",
          tension: 0.1
        },
        {
          label: "Food",
          data: j.map(j => j.food),
          fill: false,
          borderColor: "green",
          tension: 0.1
        },
        {
          label: "Stress",
          data: j.map(j => j.stress),
          fill: false,
          borderColor: "black",
          tension: 0.1
        }
      ];
    }
  },
  actions: {
    loadGoalTrees(context) {
      const wrapper = wrap(context);
      goals.loadList().subscribe(c => wrapper.commit("setGoalTrees", c));
    },
    createGoalTree(context, name) {
      const wrapper = wrap(context);
      wrapper.commit("startUploadingData");
      goals.createTree(name).subscribe({
        next: result => {
          wrapper.commit("addGoalTree", result);
          wrapper.commit("setCurrentGoalTree", result.id);
        },
        complete: () => wrapper.commit("finishUploadingData")
      });
    },
    loadGoalTree(context) {
      const wrapper = wrap(context);
      const id = context.state.currentGoalTree;
      if (id != undefined) {
        wrapper.commit("startUploadingData");
        goals.loadFullTree(id).subscribe({
          next: result => wrapper.commit("setFullGoalTree", result),
          complete: () => wrapper.commit("finishUploadingData")
        });
      }
    },
    createNewGoalTreeNode(context, node) {
      const wrapper = wrap(context);
      const id = context.state.currentGoalTree;
      if (id != undefined) {
        wrapper.commit("startUploadingData");
        goals.createTreeNode(id, "New node", node).subscribe({
          next: result => wrapper.commit("addNewGoalTreeNode", result),
          complete: () => wrapper.commit("finishUploadingData")
        });
      }
    },
    moveGoalTreeNodeTo(context, { movedNode, targetNode }) {
      const wrapper = wrap(context);
      const id = context.state.currentGoalTree;
      if (
        id != undefined &&
        movedNode != undefined &&
        targetNode !== undefined
      ) {
        wrapper.commit("startUploadingData");
        goals.moveNode(id, movedNode, targetNode).subscribe({
          next: result => wrapper.commit("setFullGoalTree", result),
          complete: () => wrapper.commit("finishUploadingData")
        });
      }
    },
    editGoalTreeNode(context, editedNode) {
      const wrapper = wrap(context);
      const id = context.state.currentGoalTree;
      if (id != undefined) {
        wrapper.commit("startUploadingData");
        goals
          .editNode(id, editedNode.id, editedNode.title, editedNode.description)
          .subscribe({
            next: result => wrapper.commit("editGoalTreeNode", result),
            complete: () => wrapper.commit("finishUploadingData")
          });
      }
    },
    deleteGoalTreeNode(context, nodeId) {
      const wrapper = wrap(context);
      const id = context.state.currentGoalTree;
      if (id != undefined) {
        wrapper.commit("startUploadingData");
        goals.deleteNode(id, nodeId).subscribe({
          next: result => wrapper.commit("setFullGoalTree", result),
          complete: () => wrapper.commit("finishUploadingData")
        });
      }
    },
    loadCategories(context) {
      const wrapper = wrap(context);
      notes.loadCategories().subscribe(c => wrapper.commit("setCategories", c));
    },
    createCategory(context, name) {
      const wrapper = wrap(context);
      wrapper.commit("startUploadingData");
      notes.newCategory(name).subscribe({
        next: result => {
          wrapper.commit("addCategory", result);
          wrapper.commit("setCurrentCategory", result.id);
        },
        complete: () => wrapper.commit("finishUploadingData")
      });
    },
    loadNotes(context) {
      const wrapper = wrap(context);

      const c = context.getters.currentCategory;
      if (c !== undefined) {
        wrapper.commit("startLoadingNotes");
        notes
          .loadNotes(c.id)
          .subscribe(notes => wrapper.commit("setNotes", notes));
      }
    },
    loadJournal(context) {
      const wrapper = wrap(context);
      wrapper.commit("startLoadingJournal");
      journal
        .loadJournal(0)
        .subscribe(entries => wrapper.commit("setJournal", entries));
    },
    createNote(context, message) {
      const wrapper = wrap(context);

      const c = context.getters.currentCategory;
      if (c !== undefined) {
        wrapper.commit("startUploadingData");
        notes.create(c.id, message).subscribe({
          next: result =>
            result.whenResult(note => wrapper.commit("addNote", note)),
          complete: () => wrapper.commit("finishUploadingData")
        });
      }
    },
    createJournalEntry(context, { message, additional }) {
      const wrapper = wrap(context);
      wrapper.commit("startUploadingData");
      journal.create(0, message, additional).subscribe({
        next: result =>
          result.whenResult(entry => wrapper.commit("addJournalEntry", entry)),
        complete: () => wrapper.commit("finishUploadingData")
      });
    },
    resolveNote(context, noteId) {
      const wrapper = wrap(context);
      wrapper.commit("startUploadingData");
      notes.resolveNote(noteId).subscribe({
        next: result =>
          result.whenResult(note => wrapper.commit("updateNote", note)),
        complete: () => wrapper.commit("finishUploadingData")
      });
    }
  }
});

auth.tokens$
  .pipe(
    filter(notNull),
    flatMap(() => users.loadUser())
  )
  .subscribe(user => store.commit("signedIn", user));

auth.tokens$
  .pipe(
    filter(notNull),
    filter(
      tokens =>
        (tokens?.accessToken || "") === "" &&
        (tokens?.refreshToken || "") !== ""
    )
  )
  .subscribe(() => store.commit("authPending"));

auth.tokens$.pipe(filter(isNull)).subscribe(() => store.commit("signedOut"));

new Vue({
  el: "#app",
  store,
  router,
  render: h => h(app)
});
