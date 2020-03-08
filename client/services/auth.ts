import {
  BehaviorSubject,
  Observable,
  of,
  combineLatest,
  throwError
} from "rxjs";
import { flatMap, filter, map, take, tap } from "rxjs/operators";
import { environment } from "../environment";
import { isDefined } from "../utility/observables";
import jwt_decode from "jwt-decode"; // eslint-disable-line
import CryptoJS from "crypto-js";
import { AppStorage } from "./storage";
import { injectable } from "inversify";
import { HttpBase, IAccessProvider } from "./http-base";
import { ISecretProvider } from "./isecret-provider";

type AuthDTO = {
  accessToken: string;
  refreshToken: string;
};

type RefreshDTO = {
  accessToken: string;
  refreshToken: string;
};

type MessageDTO = {
  msg: string;
};

function getRandomIntInclusive(min: number, max: number): number {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

class NoAccessProvider implements IAccessProvider {
  accessToken = (): Observable<string> => of("");
}

@injectable()
export class Auth extends HttpBase implements IAccessProvider, ISecretProvider {
  tokens = new BehaviorSubject<AuthDTO | null | undefined>(undefined);
  secret = new BehaviorSubject<string>("");
  tokens$ = this.tokens.asObservable();
  clientIdentity: number;

  constructor(private storage: AppStorage) {
    super(new NoAccessProvider(), environment.host);

    const refreshToken = this.storage.state.auth.refreshToken;
    const secret = this.storage.state.auth.secret;
    const clientIdentity = this.storage.state.auth.clientIdentity;
    if (refreshToken && secret && clientIdentity) {
      this.tokens.next({
        accessToken: "",
        refreshToken
      });
      this.secret.next(secret);
      this.clientIdentity = clientIdentity;
    } else {
      this.clientIdentity = getRandomIntInclusive(0, 999999999);
    }

    combineLatest([this.tokens$, this.secret.asObservable()]).subscribe(
      ([tokens, secret]) => {
        this.storage.state.auth.refreshToken = tokens?.refreshToken || null;
        this.storage.state.auth.secret = secret;
        this.storage.state.auth.clientIdentity = this.clientIdentity;
        this.storage.update();
      }
    );
  }

  login(username: string, password: string): void {
    this.request<AuthDTO>("POST", "/login", {
      isAuthenticated: false,
      body: {
        username,
        password,
        client: this.clientIdentity
      }
    }).subscribe(r => {
      this.tokens.next(r.getOrValue(null));
      this.secret.next(CryptoJS.SHA3("lappuzet" + password).toString());
    });
  }

  refresh(): Observable<AuthDTO | null> {
    return this.tokens$
      .pipe(
        take(1),
        filter(isDefined),
        flatMap(tokens =>
          this.request<RefreshDTO>("POST", "/refresh", {
            isAuthenticated: false,
            headers: { Authorization: "Bearer " + tokens.refreshToken }
          }).pipe(
            map(result =>
              result
                .map(
                  refresh =>
                    ({
                      accessToken: refresh.accessToken,
                      refreshToken: refresh.refreshToken
                    } as AuthDTO)
                )
                .getOrValue(null)
            )
          )
        )
      )
      .pipe(tap(tokens => this.tokens.next(tokens)));
  }

  logout(): void {
    this.accessToken()
      .pipe(
        take(1),
        flatMap(token => {
          if (token === "") {
            return throwError("no access token");
          }

          return this.request<MessageDTO>("DELETE", "/logout", {
            isAuthenticated: false,
            headers: { Authorization: "Bearer " + token }
          });
        })
      )
      .subscribe(() => {
        this.tokens.next(null);
        this.secret.next("");
      });
  }

  accessToken(): Observable<string> {
    return this.tokens$.pipe(
      take(1),
      flatMap(tokens =>
        tokens !== null && tokens !== undefined && this.isExpired(tokens)
          ? this.refresh()
          : of(tokens)
      ),
      map(tokens => (tokens && tokens.accessToken) || "")
    );
  }

  secretToken(): string {
    return this.secret.getValue();
  }

  isExpired(tokens: AuthDTO): boolean {
    if (!tokens.accessToken) {
      return true;
    }

    const exp = (jwt_decode(tokens.accessToken) as { exp: number }).exp;
    return Date.now() >= exp * 1000;
  }
}
