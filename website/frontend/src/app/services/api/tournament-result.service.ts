import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { TournamentResult } from '../../models/api/tournament-result.model';

@Injectable({
  providedIn: 'root'
})
export class TournamentResultService {
  constructor(private http: HttpClient) {}

  getTournamentResult(tournamentId: number): Observable<any> {
    console.log('id:', tournamentId);
    return this.http.get<TournamentResult>(`app/tournament/${tournamentId}/results`);
  }
}
