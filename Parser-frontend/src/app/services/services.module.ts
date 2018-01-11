import { NgModule } from '@angular/core';
import { HttpService } from './http.service';
import { ParserService } from './parser.service';


@NgModule({
    providers: [
        HttpService,
        ParserService
    ]
})
export class ServicesModule {
}
