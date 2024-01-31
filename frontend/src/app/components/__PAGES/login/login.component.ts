import {Component, OnInit} from '@angular/core';
import {LoginService} from "../../../services/api/login.service";
import {ProfileService} from "../../../services/profile.service";
import {ActivatedRoute, Router} from "@angular/router";

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

    constructor(
        private router: Router,
        private login_service: LoginService,
        private profile_service: ProfileService,
    ) {
    }

    ngOnInit(): void {
    }

    login(): void {
        // @ts-ignore
        let email = document.getElementById('email').value;
        // @ts-ignore
        let password = document.getElementById('password').value;
    }

    show_text(id: string) {
        let el = document.getElementById(id)!;
        // @ts-ignore
        if (el.type == 'password') el.type='text';
        else { // @ts-ignore
            el.type = 'password';
        }
    }

    go(link: string) {
        this.router.navigate([link]);
    }
}
