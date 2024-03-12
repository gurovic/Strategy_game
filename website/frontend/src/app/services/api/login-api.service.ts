import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {UserLogin} from "../../models/api/user-login.model";
import {baseUrl} from "../../interface/utils";

const currentUrl = `/accounts/login/`;

@Injectable({
  providedIn: 'root'
})
export class LoginApiService {

  constructor(
    private http: HttpClient,
  ) {
  }

  create(data: any): Observable<any> {
    return this.http.post(`${currentUrl}`, data);
  }
}
