import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {UserRegister} from "../../models/api/user-register.model";


const baseUrl = '/api/register/';

@Injectable({
    providedIn: 'root'
})
export class RegisterApiService {

    constructor(private http: HttpClient) {
    }

    getAll(): Observable<UserRegister[]> {
        return this.http.get<UserRegister[]>(baseUrl);
    }

    get(id: any): Observable<UserRegister> {
        return this.http.get(`${baseUrl}${id}`);
    }

    create(data: any): Observable<any> {
        return this.http.post(`${baseUrl}`, data);
    }

    delete(id: any): Observable<any> {
        return this.http.delete(`${baseUrl}${id}`);
    }
}
