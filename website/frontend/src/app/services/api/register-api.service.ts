import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { UserRegister } from "../../models/api/user-register.model";
import {baseUrl} from "../../interface/utils";


const currentUrl = `/register/`;

@Injectable({
  providedIn: 'root'
})
export class RegisterApiService {

  constructor(private http: HttpClient) { }

  getAll(): Observable<UserRegister[]> {
    return this.http.get<UserRegister[]>(currentUrl);
  }

  get(id: any): Observable<UserRegister> {
    return this.http.get(`${currentUrl}${id}`);
  }

  create(data: any): Observable<any> {
    return this.http.post(`${currentUrl}`, data);
  }

  delete(id: any): Observable<any> {
    return this.http.delete(`${currentUrl}${id}`);
  }
}
