import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Title } from '@angular/platform-browser';

import { TournamentResultService } from '../../../services/api/tournament-result.service';
import { TournamentResult, PlayerInTournament } from '../../../models/api/tournament-result.model';
@Component({
  selector: 'app-tournament-result',
  templateUrl: './tournament-result.component.html',
  styleUrls: ['./tournament-result.component.scss']
})
export class TournamentResultComponent implements OnInit {
  tournamentResult: TournamentResult | null = null;
  currentPage: number = 0;
  pageSize: number = 50;

  constructor(
    private route: ActivatedRoute,
    private tournamentResultService: TournamentResultService,
    private titleService: Title
  ) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      let id = params.get('tournamentId');
      if (id !== null) {
        this.loadTournamentResult(parseInt(id));
      }
    });
  }

  loadTournamentResult(tournamentId: number): void {
  this.tournamentResultService.getTournamentResult(tournamentId)
    .subscribe(
      resp => {
        console.log(resp);
        this.tournamentResult = resp;
        if (this.tournamentResult?.tournament?.name) {
          this.titleService.setTitle(`${this.tournamentResult.tournament.name}`);
        }
      },
      error => {
        console.error('Error loading tournament result:', error);
      }
    );
}

  get displayedParticipants(): PlayerInTournament[] {
    if (!this.tournamentResult || !this.tournamentResult.playersInTournament) {
      return [];
    }
    const startIndex = this.currentPage * this.pageSize;
    return this.tournamentResult.playersInTournament.slice(startIndex, startIndex + this.pageSize);
  }

  get maxPage(): number {
    if (!this.tournamentResult || !this.tournamentResult.playersInTournament) {
      return 0;
    }
    return Math.ceil(this.tournamentResult.playersInTournament.length / this.pageSize) - 1;
  }

  nextPage(): void {
    if (this.currentPage < this.maxPage) {
      this.currentPage++;
    }
  }

  prevPage(): void {
    if (this.currentPage > 0) {
      this.currentPage--;
    }
  }
}
