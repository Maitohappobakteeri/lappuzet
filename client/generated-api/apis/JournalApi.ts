// tslint:disable
/**
 * Lappuzet
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.0.1
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { Observable } from 'rxjs';
import { BaseAPI, HttpHeaders, HttpQuery, throwIfNullOrUndefined, encodeURI, OperationOpts, RawAjaxResponse } from '../runtime';
import {
    NewJournalNoteDto,
    OwnJournalNoteDto,
} from '../models';

export interface LoadHistoryRequest {
    start: number;
    amount: number;
}

export interface NewNoteRequest {
    categoryId: number;
    newJournalNoteDto: NewJournalNoteDto;
}

/**
 * no description
 */
export class JournalApi extends BaseAPI {

    /**
     * Gets journal notes
     */
    loadHistory({ start, amount }: LoadHistoryRequest): Observable<Array<OwnJournalNoteDto>>
    loadHistory({ start, amount }: LoadHistoryRequest, opts?: OperationOpts): Observable<RawAjaxResponse<Array<OwnJournalNoteDto>>>
    loadHistory({ start, amount }: LoadHistoryRequest, opts?: OperationOpts): Observable<Array<OwnJournalNoteDto> | RawAjaxResponse<Array<OwnJournalNoteDto>>> {
        throwIfNullOrUndefined(start, 'start', 'loadHistory');
        throwIfNullOrUndefined(amount, 'amount', 'loadHistory');

        const query: HttpQuery = { // required parameters are used directly since they are already checked by throwIfNullOrUndefined
            'start': start,
            'amount': amount,
        };

        return this.request<Array<OwnJournalNoteDto>>({
            url: '/journal/category/history',
            method: 'GET',
            query,
        }, opts?.responseOpts);
    };

    /**
     * Creates a new journal note
     */
    newNote({ categoryId, newJournalNoteDto }: NewNoteRequest): Observable<OwnJournalNoteDto>
    newNote({ categoryId, newJournalNoteDto }: NewNoteRequest, opts?: OperationOpts): Observable<RawAjaxResponse<OwnJournalNoteDto>>
    newNote({ categoryId, newJournalNoteDto }: NewNoteRequest, opts?: OperationOpts): Observable<OwnJournalNoteDto | RawAjaxResponse<OwnJournalNoteDto>> {
        throwIfNullOrUndefined(categoryId, 'categoryId', 'newNote');
        throwIfNullOrUndefined(newJournalNoteDto, 'newJournalNoteDto', 'newNote');

        const headers: HttpHeaders = {
            'Content-Type': 'application/json',
        };

        return this.request<OwnJournalNoteDto>({
            url: '/journal/category/new'.replace('{categoryId}', encodeURI(categoryId)),
            method: 'POST',
            headers,
            body: newJournalNoteDto,
        }, opts?.responseOpts);
    };

}
