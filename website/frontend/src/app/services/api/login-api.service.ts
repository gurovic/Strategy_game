import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {UserLogin} from "../../models/api/user-login.model";

const currentUrl = `/app/login/`;

@Injectable({
  providedIn: 'root'
})
export class LoginApiService {

  constructor(
    private http: HttpClient,
  ) {
  }

  IsAuthorized() {
    const token: string = localStorage.getItem('token')!;
    console.log(token);
    if (token == null) return false;
    return true;
  }

  create(data: UserLogin): Observable<any> {
    return this.http.post(`${currentUrl}`, data);
  }
}
