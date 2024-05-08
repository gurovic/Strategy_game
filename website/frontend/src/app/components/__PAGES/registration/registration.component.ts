import {Component, OnInit} from '@angular/core';
import {RegisterApiService} from "../../../services/api/register-api.service";
import {UserRegister} from "../../../models/api/user-register.model";
import {Router} from "@angular/router";
import {ProfileApiService} from "../../../services/api/profile-api.service";
import {LoaderComponentComponent} from "../../__MODELS/loader-component/loader-component.component";

@Component({
    selector: 'app-registration',
    templateUrl: './registration.component.html',
    styleUrls: ['./registration.component.scss', '../login/login.component.scss']
})
export class RegistrationComponent implements OnInit {
    public user: UserRegister = {username: '', password1: '', email: '', password2: ''};

    constructor(
        public register_service: RegisterApiService,
        private profile_api_service: ProfileApiService,
        private router: Router,
    ) {
    }

    ngOnInit(): void {
        this.profile_api_service.get().subscribe(
            resp => {
                this.router.navigate(['profile']);
            }
        );
    }

    register() {
        LoaderComponentComponent.Show();
        this.register_service.create(this.user).subscribe(
            resp => {
                LoaderComponentComponent.Hide();
                location.reload();
                localStorage.setItem('token', '2147h4247y329j43298423h98j9');
                this.router.navigate(['']).then();
            },
            error => {
                LoaderComponentComponent.Hide();
            },
        )
    }

    go_link(link: string) {
        this.router.navigate([link]);
    }

}
