import { Component, OnInit } from '@angular/core';
import {TournamentModel} from "../../../models/api/tournament.model";
import {ActivatedRoute} from "@angular/router";
import {TournamentApiService} from "../../../services/api/tournament-api.service";

@Component({
  selector: 'app-tournament-solution-upload',
  templateUrl: './tournament-solution-upload.component.html',
  styleUrls: ['./tournament-solution-upload.component.scss']
})
export class TournamentSolutionUploadComponent implements OnInit {
  public tournament: TournamentModel | undefined;

  constructor(
    private route: ActivatedRoute,
    private tournament_api_service: TournamentApiService,
  ) { }

  ngOnInit(): void {
    this.get_tournament();
  }

  get_tournament() {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.tournament_api_service.get().subscribe(resp=>{
      for (const x of resp.future) {
        if (x.id == id) {
          this.tournament = {
            name: x.name,
            id: x.id,
            start_date: x.tournament_start_time,
            participants: x.max_of_players,
            
          }
        }
        console.log(x);
      }
    })
  }
}
