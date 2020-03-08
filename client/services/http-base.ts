import { Observable, from, of } from "rxjs";
import { ResultEither } from "./result-either";
import { map, catchError } from "rxjs/operators";

export const InjAccessProvider = Symbol.for("IAccessTokenProvider");

export interface IAccessProvider {
  accessToken(): Observable<string>;
}

export interface Headers {
  "Content-Type"?: string;
  Authorization?: string;
}

export interface IRequestOptions {
  isAuthenticated: boolean;
  headers: Record<string, string>;
  body?: any; //eslint-disable-line
}

export const DefaultRequestOptions: IRequestOptions = {
  isAuthenticated: true,
  headers: {}
};

export class HttpBase {
  constructor(
    protected accessProvider: IAccessProvider,
    protected baseURL: string
  ) {}

  request<T>(
    method: "POST" | "PUT" | "GET" | "DELETE",
    resource: string,
    customOptions: Partial<IRequestOptions> = {}
  ): Observable<ResultEither<T, string>> {
    const options = {
      ...DefaultRequestOptions,
      ...customOptions
    };

    return from(
      (async () => {
        // Headers
        const headers: Record<string, string> = {
          "Content-Type": "application/json",
          ...options.headers
        };
        if (options.isAuthenticated) {
          const token = await this.accessProvider.accessToken().toPromise();
          if (token === "") {
            return null;
          }

          headers["Authorization"] = "Bearer " + token;
        }

        // Do request
        return await fetch(this.baseURL + resource, {
          method,
          cache: "no-cache",
          headers,
          // TODO: This is hard to read and this shouldn't throw error and
          //       instead return a Either type of struct
          body: options.body && JSON.stringify(options.body)
        }).then(response => {
          // Map response
          if (!response.ok) {
            throw new Error(response.statusText);
          }
          return response.json();
        });
      })()
    ).pipe(
      map(r => ResultEither.result<T, string>(r)),
      catchError(e => of(ResultEither.error<T, string>(e)))
    );
  }
}
