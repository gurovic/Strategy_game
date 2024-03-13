import {Injectable} from '@angular/core';
import {Profile} from "../models/profile.model";

@Injectable({
    providedIn: 'root'
})
export class ProfileService {
    public user: Profile = { is_registered: false };

    constructor() {
    }

    get_user(): Profile { return this.user; }
    set_user(user: any) {
        this.user.email = user.email;
        this.user.username = user.username;
        this.user.first_name = user.first_name;
        this.user.is_registered = true;
        this.user.last_name = user.last_name;
        this.user.date_joined = user.date_joined;
    }
    clear() {
        this.user = {is_registered: false};
    }
}
