import { Component, OnInit } from '@angular/core';
import {FormControl, FormsModule, FormBuilder} from "@angular/forms";
import {GameUploadService} from "../../../services/game-upload.service";


@Component({
  selector: 'app-upload-game',
  templateUrl: './upload-game.component.html',
  styleUrls: ['./upload-game.component.scss']
})
export class UploadGameComponent implements OnInit {
  checkoutForm: any;

  constructor(
      private formBuilder: FormBuilder,
      private gameUploadService: GameUploadService
  ) {
    this.checkoutForm = this.formBuilder.group({
      name: '',
      number_of_players: '',
      ideal_solution: '',
      play: '',
      win_point: '',
      lose_point: '',
      visualiser: '',
      rules: ''
    });
  }

  ngOnInit(): void {
  }

  onSubmit() {
    console.log(this.checkoutForm.value);
    this.gameUploadService.uploadingGame(this.checkoutForm.value).subscribe({
      next: value => console.log('Your files compiled successfully! Congratulations!'),
      error: err => console.error('Compilation failed'),
    });
  }
}
