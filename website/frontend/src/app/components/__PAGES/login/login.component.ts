import {Component, OnInit} from '@angular/core';
import {LoginApiService} from "../../../services/api/login-api.service";
import {Router} from "@angular/router";
import {UserLogin} from "../../../models/api/user-login.model";
import {RegisterApiService} from "../../../services/api/register-api.service";
import {UserRegister} from "../../../models/api/user-register.model";
import {ProfileService} from "../../../services/profile.service";
import {ProfileApiService} from "../../../services/api/profile-api.service";
import {RoutingService} from "../../../services/routing.service";

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
    public user: UserLogin = {username: '', password: ''};

    constructor(
        private login_service: LoginApiService,
        private profile_service: ProfileService,
        private profile_api_service: ProfileApiService,
        private router: RoutingService,
    ) {
    }

    ngOnInit(): void {
        this.profile_api_service.get().subscribe(
            resp => {
                this.router.navigate('profile');
            }
        );
    }

    login() {
        // @ts-ignore
        document.getElementById('loader-box').style.display = 'flex';
        this.login_service.create(this.user).subscribe(
            resp => {
                this.profile_api_service.get().subscribe(
                    response => {
                        this.profile_service.set_user(response);
                        setTimeout(() => {
                            // @ts-ignore
                            document.getElementById('loader-box').style.display = 'none';
                            this.router.navigate('profile')
                            location.reload();
                        }, 1000)
                    },
                    error => {
                        // @ts-ignore
                        document.getElementById('loader-box').style.display = 'none';
                        this.profile_service.clear();
                    },
                )
            },
            error => {
                // @ts-ignore
                document.getElementById('loader-box').style.display = 'none';
                this.profile_service.clear()
            },
        )
    }

    forgot_password() {
        //TODO
    }

    go_link(link: string) {
        this.router.navigate(link);
        window.scrollTo({
            // @ts-ignore
            top: 0,
            behavior: "smooth"
        });
    }
}
