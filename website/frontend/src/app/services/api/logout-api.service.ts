import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';

const currentUrl = `/app/logout/`;

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
