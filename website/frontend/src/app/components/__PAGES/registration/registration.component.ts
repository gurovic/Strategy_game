import {Component, OnInit} from '@angular/core';
import {RegisterApiService} from "../../../services/api/register-api.service";
import {UserRegister} from "../../../models/api/user-register.model";
import {Router} from "@angular/router";
import {ProfileService} from "../../../services/profile.service";
import {ProfileApiService} from "../../../services/api/profile-api.service";

@Component({
    selector: 'app-registration',
    templateUrl: './registration.component.html',
    styleUrls: ['./registration.component.scss', '../login/login.component.scss']
})
export class RegistrationComponent implements OnInit {
    public user: UserRegister = {username: '', password1: '', email: '', password2: ''};

    constructor(
        public register_service: RegisterApiService,
        private profile_service: ProfileService,
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
        this.register_service.create(this.user).subscribe(
            resp => {
                this.profile_api_service.get().subscribe(
                    response => {
                        this.profile_service.set_user(response);
                        setTimeout(() => {
                            // @ts-ignore
                            document.getElementById('loader-box').style.display = 'none';
                            this.router.navigate(['profile'])
                            location.reload();
                        }, 1000)
                    },
                    error => {
                        // @ts-ignore
                        document.getElementById('loader-box').style.display = 'none';
                    },
                )
            },
            error => {
                // @ts-ignore
                document.getElementById('loader-box').style.display = 'none';
            },
        )
    }

    go_link(link: string) {
        this.router.navigate([link]);
    }

}
