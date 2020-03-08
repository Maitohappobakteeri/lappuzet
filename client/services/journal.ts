import { environment } from "../environment";
import { map } from "rxjs/operators";
import { Observable } from "rxjs";
import aes from "crypto-js/aes";
import CryptoJS from "crypto-js";
import { injectable, inject } from "inversify";
import { InjAccessProvider, IAccessProvider } from "./http-base";
import { InjSecretProvider, ISecretProvider } from "./isecret-provider";
import { ResultEither } from "./result-either";
import { OwnJournalNoteDto } from "../generated-api/models";
import { JournalApi } from "../generated-api";

export type JournalEntry = {
  id: number;
  message: string;
  createdAt: Date;

  mood: number;
  sleep: number;
  stress: number;
  food: number;
};

@injectable()
export class JournalService {
  private journalApi: JournalApi;

  constructor(
    @inject(InjAccessProvider) accessProvider: IAccessProvider,
    @inject(InjSecretProvider) private secretProvider: ISecretProvider
  ) {
    this.journalApi = new JournalApi(accessProvider, environment.host);
  }

  create(
    categoryId: number,
    message: string,
    additional: {
      mood: number;
      sleep: number;
      stress: number;
      food: number;
    }
  ): Observable<ResultEither<JournalEntry, string>> {
    return this.journalApi
      .newNote({
        newJournalNoteDto: {
          message: aes
            .encrypt(message, this.secretProvider.secretToken())
            .toString(),
          ...additional
        },
        categoryId
      })
      .pipe(map(j => ResultEither.result(this.entryFromDTO(j))));
  }

  loadJournal(categoryId: number): Observable<JournalEntry[]> {
    return this.loadHistory(categoryId).pipe(
      map(dtos => dtos.map(dto => this.entryFromDTO(dto)))
    );
  }

  loadHistory(categoryId: number): Observable<OwnJournalNoteDto[]> {
    return this.journalApi.loadHistory({ start: 0, amount: 50 });
  }

  entryFromDTO(d: OwnJournalNoteDto): JournalEntry {
    return {
      id: d.id,
      message: aes
        .decrypt(d.message, this.secretProvider.secretToken())
        .toString(CryptoJS.enc.Utf8),
      createdAt: new Date(d.created_at),

      stress: d.journal_note_additional.stress,
      sleep: d.journal_note_additional.sleep,
      food: d.journal_note_additional.food,
      mood: d.journal_note_additional.mood
    };
  }
}
