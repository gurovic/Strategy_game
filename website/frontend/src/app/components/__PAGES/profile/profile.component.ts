import {Component, OnInit, ViewChild} from '@angular/core';
import {Profile} from "../../../models/profile.model";
import {ActivatedRoute, Router} from "@angular/router";
import {ProfileApiService} from "../../../services/api/profile-api.service";
import {LogoutApiService} from "../../../services/api/logout-api.service";
import {LoaderComponentComponent} from "../../__MODELS/loader-component/loader-component.component";

@Component({
    selector: 'app-profile',
    templateUrl: './profile.component.html',
    styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
    public user: Profile = {is_registered: false};
    @ViewChild('username') public username_container: any;
    @ViewChild('last_name') public last_name_container: any;
    @ViewChild('email') public email_container: any;
    @ViewChild('first_name') public first_name_container: any;
    @ViewChild('date_joined') public date_joined_container: any;

    constructor(
        private router: Router,
        private profile_api_service: ProfileApiService,
        private logout_api_service: LogoutApiService,
    ) {
    }

    ngOnInit(): void {
        LoaderComponentComponent.Show();
        this.profile_api_service.get().subscribe(
            resp => {
                LoaderComponentComponent.Hide();
                this.user = resp;
                this.user.is_registered = true;
                this.username_container.nativeElement.innerText = this.user.username;
                this.email_container.nativeElement.innerText = this.user.email;
                this.first_name_container.nativeElement.innerText = this.user.first_name;
                this.last_name_container.nativeElement.innerText = this.user.last_name;
                this.date_joined_container.nativeElement.innerText = this.user.date_joined;
            },
            error => {
                LoaderComponentComponent.Hide();
                this.router.navigate(['login']);
            },
        )
    }

    logout() {
        this.logout_api_service.post('').subscribe(
            resp => {
                location.reload();
            },
        )
        this.router.navigate(['']);
    }
}
