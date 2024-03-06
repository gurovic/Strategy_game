import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Logout} from "../../models/api/logout.model";

const baseUrl = '/api/logout/';

@Injectable({
  providedIn: 'root'
})
export class LogoutService {

  constructor(
    private http: HttpClient
  ) {}

  post(data: any): Observable<any> {
    return this.http.post(`${baseUrl}`, data);
  }
}
