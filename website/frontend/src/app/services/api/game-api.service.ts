import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class GameApiService {

  constructor(
      private http: HttpClient
  ) { }

  get_by_id(id: number): Observable<any> {
    return this.http.get(`app/game/${id}`);
  }
}
