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
    }
}
