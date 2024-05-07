import {Component, OnInit, ViewChild} from '@angular/core';
import {FormControl, FormsModule, FormBuilder} from "@angular/forms";
import {GameUploadService} from "../../../services/game-upload.service";
import {NotifierService} from "angular-notifier";
import {Router} from "@angular/router";


@Component({
    selector: 'app-upload-game',
    templateUrl: './upload-game.component.html',
    styleUrls: ['./upload-game.component.scss']
})
export class UploadGameComponent implements OnInit {
    checkoutForm: any;

    constructor(
        private formBuilder: FormBuilder,
        private gameUploadService: GameUploadService,
        private notifierService: NotifierService,
        private router: Router,
    ) {
    }

    ngOnInit(): void {
        this.checkoutForm = this.formBuilder.group({
            name: '',
            number_of_players: null,
            ideal_solution: null,
            play: null,
            win_point: null,
            lose_point: null,
            visualiser: null,
            rules: null
        });
    }

    uploadFile(event: any) {
        this.checkoutForm.get(event.target!.name).setValue(event.target!.files[0]);
    }

    onSubmit() {
        this.gameUploadService.uploadingGame(this.checkoutForm.value).subscribe(
            resp => {
                this.notifierService.notify('sucsess', 'Новая игра была создана');
            }, error => {
                this.notifierService.notify('error', 'Ой, что-то пошло не так');
            }
        );
    }
}
