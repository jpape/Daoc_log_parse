import { Injectable } from '@angular/core';
import { Response, RequestOptions, Headers } from '@angular/http';
import { Observable, Subject } from 'rxjs';

import { HttpService } from './http.service';


@Injectable()
export class ParserService {

  constructor(
    private httpService: HttpService
  ) { }

  sendFileToParse(file) : Observable<Response> {
    let formData:FormData = new FormData();
    formData.append('logfile', file, file.name);
    let optHeaders = new Headers();
    // optHeaders.append('Content-Type', 'multipart/form-data');
    optHeaders.append('Accept', 'application/json');
    let options = new RequestOptions({ headers: optHeaders});
    return this.httpService.post('http://127.0.0.1:5000/upload', formData, options)
      .map((response: Response) => {
        let res = response.json();
        return res;
      });
  }


}
