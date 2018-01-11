import { Component, OnInit, Input, HostListener } from '@angular/core';
import { FormsModule, FormGroup, FormBuilder, FormControl, Validators, ReactiveFormsModule } from '@angular/forms';
import { FileDropModule, UploadFile, UploadEvent } from 'ngx-file-drop';
import { ParserService } from './services/parser.service';

import { ParsingResults } from '../models/parse-results.model';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
  
  @Input() fileExt: string = "TXT, LOG";

  constructor(
    private formBuilder: FormBuilder,
    private parserService: ParserService
  ) {}

  parsedLogForm: FormGroup;
  files: UploadFile[] = [];
  resultsForPage: ParsingResults;
  healingTargets: string[]
  healingSources: string[]
  castingTargets: string[]
  meleeTargets: string[]
  defenseSources: string[]


  ngOnInit() {
    this.buildEmptyForm();
  }


  buildEmptyForm() {
    this.parsedLogForm = this.formBuilder.group({
      combatDefenseSources: [''],

      combatAttackSpellTargets: [''],

      combatAttackMeleeTargets: [''],

      healingSources: [''],
      healingTargets: ['']
    })
  }

  onFileUploaded(event: UploadEvent) {
    let file = event.files[0];
    this.parserService.sendFileToParse(file)
      .subscribe(
        (results: any) => {
          let castedResults = results as ParsingResults;
          alert(castedResults);
        }
      )
  }

  dropped(event: UploadEvent) {
    this.files = event.files;
    for (var file of event.files) {
      file.fileEntry.file(info => {
        console.log(info);
      });
    }
  }

  fileChange(event) {
    let fileList: FileList = event.target.files;
    let file = fileList[0];
    this.parserService.sendFileToParse(file)
      .subscribe(
        (results: any) => {
          let castedResults = results as ParsingResults;
          if (castedResults) {
            this.healingSources = castedResults.Healing.Sources;
            this.healingTargets = castedResults.Healing.Targets;
            this.castingTargets = castedResults.Combat.CasterAttack.Targets;
            this.meleeTargets = castedResults.Combat.MeleeAttack.Targets;
            this.defenseSources = castedResults.Combat.Defense.Sources;
            this.resultsForPage = castedResults;
            this.updateFormWithResults(castedResults);
          }
        }
      )
  }


  updateFormWithResults(parsedResults: ParsingResults) {
    this.parsedLogForm.patchValue({
      combatDefenseSources: parsedResults.Combat.Defense.Sources,

      combatAttackSpellTargets: parsedResults.Combat.CasterAttack.Targets,

      combatAttackMeleeTargets: parsedResults.Combat.MeleeAttack.Targets,

      healingSources: parsedResults.Healing.Sources,
      healingTargets: parsedResults.Healing.Targets
    })
  }

  currencyPrintHelper(currency_dict) {
    let result_text = '';
    if (currency_dict[0] > 0) {
        result_text += currency_dict[0] + 'p ';
    } 
    if (currency_dict[1] > 0) {
        result_text += currency_dict[1] + 'g ';
    }
    if (currency_dict[2] > 0) {
        result_text += currency_dict[2] + 's ';
    }
    if (currency_dict[3] > 0) {
        result_text += currency_dict[3] + 'c';
    }
    return result_text
  }
}
