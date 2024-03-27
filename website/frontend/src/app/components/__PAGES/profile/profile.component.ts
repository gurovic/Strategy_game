import {Component, OnInit} from '@angular/core';
import {Profile} from "../../../models/profile.model";
import {ActivatedRoute, Router} from "@angular/router";
import {ProfileApiService} from "../../../services/api/profile-api.service";
import {ProfileService} from "../../../services/profile.service";
import {LogoutApiService} from "../../../services/api/logout-api.service";

@Component({
    selector: 'app-profile',
    templateUrl: './profile.component.html',
    styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
    public user: Profile = {is_registered: false};

    constructor(
        private router: Router,
        private profile_api_service: ProfileApiService,
        private logout_api_service: LogoutApiService,
        private profile_service: ProfileService,
    ) {
    }

    ngOnInit(): void {
        this.user = this.profile_service.get_user();
        if (!this.user.is_registered)
            this.profile_api_service.get().subscribe(
                resp => {
                    this.profile_service.set_user(resp);
                    this.user = this.profile_service.get_user();
                    if (!this.user.is_registered) this.router.navigate(['']);
                    // @ts-ignore
                    document.getElementById('username')!.innerText = this.user.username;
                    // @ts-ignore
                    document.getElementById('email')!.innerText = this.user.email;
                    // @ts-ignore
                    document.getElementById('first-name')!.innerText = this.user.first_name;
                    // @ts-ignore
                    document.getElementById('last-name')!.innerText = this.user.last_name;
                    // @ts-ignore
                    document.getElementById('date-joined')!.innerText = this.user.date_joined;
                },
                error => {
                    this.profile_service.clear();
                    this.router.navigate(['']);
                },
            )
        else {
            // @ts-ignore
            document.getElementById('username')!.innerText = this.user.username;
            // @ts-ignore
            document.getElementById('email')!.innerText = this.user.email;
            // @ts-ignore
            document.getElementById('first-name')!.innerText = this.user.first_name;
            // @ts-ignore
            document.getElementById('last-name')!.innerText = this.user.last_name;
            // @ts-ignore
            document.getElementById('date-joined')!.innerText = this.user.date_joined;
        }
    }

    logout() {
        this.logout_api_service.post('').subscribe(
            resp => {
                this.profile_service.clear();
                location.reload();
            },
        )
        this.router.navigate(['']);
    }
}
