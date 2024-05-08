import {Component, OnInit} from '@angular/core';
import {LoginApiService} from "../../../services/api/login-api.service";
import {Router} from "@angular/router";
import {UserLogin} from "../../../models/api/user-login.model";
import {ProfileApiService} from "../../../services/api/profile-api.service";
import {LoaderComponentComponent} from "../../__MODELS/loader-component/loader-component.component";

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
    public user: UserLogin = {username: '', password: ''};

    constructor(
        private login_service: LoginApiService,
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

    login() {
        LoaderComponentComponent.Show();
        this.login_service.create(this.user).subscribe(
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

    forgot_password() {
        //TODO
    }

    go_link(link: string) {
        this.router.navigate([link]);
        window.scrollTo({
            // @ts-ignore
            top: 0,
            behavior: "smooth"
        });
    }
}
