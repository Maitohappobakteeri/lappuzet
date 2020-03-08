import { injectable } from "inversify";

export interface StoredAuth {
  refreshToken: string | null;
  secret: string;
  clientIdentity: number | null;
}

export interface StoredState {
  version: number;
  auth: StoredAuth;

  notes: {
    selectedCategory: number | undefined;
  };

  goals: {
    selectedTree: number | undefined;
  };
}

const initialState: StoredState = {
  version: 1,

  auth: {
    refreshToken: null,
    secret: "",
    clientIdentity: null
  },

  notes: {
    selectedCategory: undefined
  },

  goals: {
    selectedTree: undefined
  }
};

@injectable()
export class AppStorage {
  state: StoredState = initialState;

  constructor() {
    const s = window.localStorage.getItem("state");
    if (s) {
      this.state = JSON.parse(s);
    }

    if (this.state.version !== initialState.version) {
      localStorage.clear();
      this.state = initialState;
    }
  }

  update(): void {
    window.localStorage.setItem("state", JSON.stringify(this.state));
  }
}
