/* tslint:disable */
/* eslint-disable */
/* Code generated by ng-openapi-gen DO NOT EDIT. */

import { HttpClient, HttpContext } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { BaseService } from '../base-service';
import { ApiConfiguration } from '../api-configuration';
import { StrictHttpResponse } from '../strict-http-response';

import { getLogs } from '../fn/log-controller/get-logs';
import { GetLogs$Params } from '../fn/log-controller/get-logs';
import { LogResponseModel } from '../models/log-response-model';

@Injectable({ providedIn: 'root' })
export class LogControllerService extends BaseService {
  constructor(config: ApiConfiguration, http: HttpClient) {
    super(config, http);
  }

  /** Path part for operation `getLogs()` */
  static readonly GetLogsPath = '/logs';

  /**
   * This method provides access to the full `HttpResponse`, allowing access to response headers.
   * To access only the response body, use `getLogs()` instead.
   *
   * This method doesn't expect any request body.
   */
  getLogs$Response(params?: GetLogs$Params, context?: HttpContext): Observable<StrictHttpResponse<Array<LogResponseModel>>> {
    return getLogs(this.http, this.rootUrl, params, context);
  }

  /**
   * This method provides access only to the response body.
   * To access the full response (for headers, for example), `getLogs$Response()` instead.
   *
   * This method doesn't expect any request body.
   */
  getLogs(params?: GetLogs$Params, context?: HttpContext): Observable<Array<LogResponseModel>> {
    return this.getLogs$Response(params, context).pipe(
      map((r: StrictHttpResponse<Array<LogResponseModel>>): Array<LogResponseModel> => r.body)
    );
  }

}
