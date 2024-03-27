import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';

const currentUrl = `/app/profile/`;

@Injectable({
    providedIn: 'root'
})
export class ProfileApiService {

    constructor(
        private http: HttpClient
    ) {
    }

    get(): Observable<any> {
        return this.http.get(`${currentUrl}`);
    }
}
