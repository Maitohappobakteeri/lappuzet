import { environment } from "../environment";
import { map, filter } from "rxjs/operators";
import { Observable, forkJoin } from "rxjs";
import aes from "crypto-js/aes";
import CryptoJS from "crypto-js";
import { injectable, inject } from "inversify";
import { InjAccessProvider, IAccessProvider } from "./http-base";
import { InjSecretProvider, ISecretProvider } from "./isecret-provider";
import { ResultEither } from "./result-either";
import { NoteApi } from "../generated-api/apis";
import { OwnNoteDto, NoteCategoryDto } from "../generated-api/models";

export type Note = {
  id: number;
  message: string;
  resolved: boolean;
  needsResolve: boolean;
  createdAt: Date;
};

@injectable()
export class NoteService {
  private noteApi: NoteApi;

  constructor(
    @inject(InjAccessProvider) accessProvider: IAccessProvider,
    @inject(InjSecretProvider) private secretProvider: ISecretProvider
  ) {
    this.noteApi = new NoteApi(accessProvider, environment.host);
  }

  create(
    categoryId: number,
    message: string
  ): Observable<ResultEither<Note, string>> {
    return this.noteApi
      .newNote({
        categoryId,
        newNoteDto: {
          message: aes
            .encrypt(message, this.secretProvider.secretToken())
            .toString(),
          needsResolve: true
        }
      })
      .pipe(map(n => ResultEither.result(this.noteFromDTO(n))));
  }

  resolveNote(noteId: number): Observable<ResultEither<Note, string>> {
    return this.noteApi
      .resolveNote({ noteId })
      .pipe(map(n => ResultEither.result(this.noteFromDTO(n))));
  }

  loadNotes(categoryId: number): Observable<Note[]> {
    return forkJoin([
      this.loadUnresolved(categoryId),
      this.loadHistory(categoryId)
    ]).pipe(
      filter(([n1, n2]) => n1 !== null && n2 !== null),
      map(([n1, n2]) => n1.concat(n2).map(d => this.noteFromDTO(d)))
    );
  }

  loadUnresolved(categoryId: number): Observable<OwnNoteDto[]> {
    return this.noteApi.loadUnresolved({ categoryId });
  }

  loadHistory(categoryId: number): Observable<OwnNoteDto[]> {
    return this.noteApi.loadHistory({ categoryId, start: 0, amount: 50 });
  }

  noteFromDTO(d: OwnNoteDto): Note {
    return {
      id: d.id,
      message: aes
        .decrypt(d.message, this.secretProvider.secretToken())
        .toString(CryptoJS.enc.Utf8),
      resolved: d.resolved,
      needsResolve: d.resolved_at === null || !d.resolved,
      createdAt: new Date(d.created_at)
    };
  }

  loadCategories(): Observable<NoteCategoryDto[]> {
    return this.noteApi.loadCategories();
  }

  newCategory(name: string): Observable<NoteCategoryDto> {
    return this.noteApi.newCategory({ newNoteCategoryDto: { name } });
  }
}
