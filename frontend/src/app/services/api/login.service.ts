import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {UserLogin} from "../../models/api/user-login.model";

const baseUrl = '/api/login/';

@Injectable({
  providedIn: 'root'
})
export class LoginService {

  constructor(
    private http: HttpClient,
  ) {
  }

  create(data: any): Observable<any> {
    return this.http.post(`${baseUrl}`, data);
  }
}
