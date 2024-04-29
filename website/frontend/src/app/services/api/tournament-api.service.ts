import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {UserLogin} from "../../models/api/user-login.model";
import {Observable} from "rxjs";

const currentUrl = '/app/tournaments/'

@Injectable({
  providedIn: 'root'
})
export class TournamentApiService {

  constructor(
    private http: HttpClient,
  ) {
  }

  get(): Observable<any> {
    return this.http.get(`${currentUrl}`);
  }

  get_by_id(id: number): Observable<any> {
    return this.http.get(`app/tournament/${id}`);
  }

  upload_solution(data: any, user_id: number, tournament_id: number): Observable<any> {
    return this.http.post<any>(`app/tournament/upload_solution/${tournament_id}/${user_id}`, data);
  }
}

