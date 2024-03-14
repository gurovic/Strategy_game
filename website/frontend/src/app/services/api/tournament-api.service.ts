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
}

