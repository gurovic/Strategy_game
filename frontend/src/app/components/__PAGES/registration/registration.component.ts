import {Component, OnInit} from '@angular/core';
import {Router} from "@angular/router";
import {LoginService} from "../../../services/api/login.service";
import {ProfileService} from "../../../services/profile.service";
import {RegisterApiService} from "../../../services/api/register.service";

@Component({
    selector: 'app-registration',
    templateUrl: './registration.component.html',
    styleUrls: ['./registration.component.scss']
})
export class RegistrationComponent implements OnInit {

    constructor(
        private router: Router,
        private profile_service: ProfileService,
        private register_service: RegisterApiService
    ) {
    }

    ngOnInit(): void {
    }

    register() {
        // @ts-ignore
        let email = document.getElementById('email').value;
        // @ts-ignore
        let username = document.getElementById('username').value;
        // @ts-ignore
        let password1 = document.getElementById('password1').value;
        // @ts-ignore
        let password2 = document.getElementById('password2').value;
    }

    show_text(id: string) {
        let el = document.getElementById(id)!;
        // @ts-ignore
        if (el.type == 'password') el.type='text';
        else { // @ts-ignore
            el.type = 'password';
        }
    }

    go(link:string) {
        this.router.navigate([link]);
    }
}
