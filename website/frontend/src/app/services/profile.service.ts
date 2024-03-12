import {Injectable} from '@angular/core';
import {Profile} from "../interface/profile";
import {local} from "d3";

@Injectable({
    providedIn: 'root'
})
export class ProfileService {

    constructor() {
    }

    get_user(): Profile {
        if (localStorage.getItem('account') != null) {
            let profile = localStorage.getItem('account')!.split(';');
            if (profile[0] == 'true') {
                return {
                    registered: true,
                    username: profile[1],
                    email: profile[2],
                };
            } else return {registered: false};
        } else return {registered: false};
    }

    register(user: Profile) {
        let account = this.get_user();
        if (account.registered) return;
        let account_string = ProfileService.make_string(user);
        localStorage.setItem('account', account_string);
    }

    logout() {
        localStorage.setItem('account', 'false');
        return;
    }


    static make_string(user: Profile): string {
        let result = ""
        if (user.registered) result += 'true;';
        else result += 'false;';

        result += user.username + ";" + user.email;
        return result;
    }
}
