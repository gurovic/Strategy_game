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

    uploadingGame(data: UploadGameModel): Observable<any> {
        let formData = new FormData();
        for (let [key, value] of Object.entries(data)) {
            formData.append(key, value);
        }
        return this.http.post('app/game_upload/form/', formData);
    }
}
