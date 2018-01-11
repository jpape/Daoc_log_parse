import { Injectable } from '@angular/core';
import { Http, Headers, Response, RequestOptionsArgs } from '@angular/http';
import { Observable, Subscription, Subject } from 'rxjs';

@Injectable()
export class HttpService {

  constructor(
    private http: Http
  ) { }

  post(url: string, body: any, options?: RequestOptionsArgs): Observable<Response> {
    return this.handleRequest(this.http.post(url, body, options));
  }

  private handleRequest(request: Observable<Response>): Observable<Response> {

    let responseSubject = new Subject<Response>();

    let requestSubscription = request
        .subscribe(r => {
            responseSubject.next(r);
        }, err => {
            // this.handleError(err);
            responseSubject.error(err);
        }, () => {
            responseSubject.complete();
        });

    // Do not expose the ISubscription portion of Subject
    return responseSubject.asObservable();
  }
}
