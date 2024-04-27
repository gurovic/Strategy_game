import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {UploadGameModel} from "../models/api/upload-game.model";
import {Observable} from "rxjs";

const currentUrl = ''

@Injectable({
    providedIn: 'root'
})
export class GameUploadService {

    constructor(
        private http: HttpClient,
    ) {
    }

    uploadingGame(data: any): Observable<any> {
        return this.http.post('app/game_upload/form/', data);
    }
}
