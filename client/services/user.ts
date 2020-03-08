import { environment } from "../environment";
import { Observable } from "rxjs";
import { injectable, inject } from "inversify";
import { HttpBase, InjAccessProvider, IAccessProvider } from "./http-base";
import { map } from "rxjs/operators";

export type User = {
  id: number;
  username: string;
};

@injectable()
export class UserService extends HttpBase {
  constructor(@inject(InjAccessProvider) accessProvider: IAccessProvider) {
    super(accessProvider, environment.host);
  }

  loadUser(): Observable<User | null> {
    return this.request<User>("GET", "/user").pipe(
      map(r => r.getOrValue(null))
    );
  }
}
