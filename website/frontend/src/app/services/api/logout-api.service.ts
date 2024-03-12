import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Logout} from "../../models/api/logout.model";
import {baseUrl} from "../../interface/utils";

const currentUrl = `${baseUrl}/logout/`;

@Injectable({
  providedIn: 'root'
})
export class LogoutApiService {

  constructor(
    private http: HttpClient
  ) {}

  post(data: any): Observable<any> {
    return this.http.post(`${currentUrl}`, data);
  }
}
