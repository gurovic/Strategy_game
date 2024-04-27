import {Component, OnInit, ViewChild} from '@angular/core';
import {FormControl, FormsModule, FormBuilder} from "@angular/forms";
import {GameUploadService} from "../../../services/game-upload.service";


@Component({
  selector: 'app-upload-game',
  templateUrl: './upload-game.component.html',
  styleUrls: ['./upload-game.component.scss']
})
export class UploadGameComponent implements OnInit {
    @ViewChild('ideal_solution_input') public ideal_solution_input: any;
    @ViewChild('play_input') public play_input: any;
    @ViewChild('rules_input') public rules_input: any;
    @ViewChild('visualizer_input') public visualizer_input: any;
    public name = '';
    public number_of_players = 0;
    public ideal_solution = undefined;
    public play = undefined;
    public win_point = 0;
    public lose_point = 0;
    public visualiser = undefined;
    public rules = undefined;

  constructor(
      private formBuilder: FormBuilder,
      private gameUploadService: GameUploadService
  ) {
  }

  ngOnInit(): void {
  }

  onSubmit(event: any) {
    this.ideal_solution = this.ideal_solution_input.nativeElement.value;
    this.visualiser = this.visualizer_input.nativeElement.value;
    this.rules = this.rules_input.nativeElement.value;
    this.play = this.play_input.nativeElement.value;
    console.log(this.name, this.ideal_solution, this.number_of_players, this.play, this.win_point, this.rules, this.lose_point, this.visualiser);
    this.gameUploadService.uploadingGame({name: this.name, ideal_solution: this.ideal_solution, play: this.play, lose_point: this.lose_point, win_point: this.win_point, rules: this.rules, visualiser: this.visualiser, number_of_players: this.number_of_players}).subscribe({
      next: value => console.log('Your files compiled successfully! Congratulations!'),
      error: err => console.error('Compilation failed'),
    });
  }
}
