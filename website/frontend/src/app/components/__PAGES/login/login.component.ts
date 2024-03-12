import { Component, OnInit } from '@angular/core';
import {LoginApiService} from "../../../services/api/login-api.service";
import {Router} from "@angular/router";
import {UserLogin} from "../../../models/api/user-login.model";
import {RegisterApiService} from "../../../services/api/register.service";
import {UserRegister} from "../../../models/api/user-register.model";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  public user: UserLogin = {username: '', password: ''};

  constructor(
      private login_service: LoginApiService,
      private router: Router,
  ) { }

  ngOnInit(): void {

  }

  login() {
    this.login_service.create(this.user).subscribe(
        resp => { console.log(resp); },
        error => { console.log(error); },
    )
  }

  go_link(link:string) {
    this.router.navigate([link]);
    window.scrollTo({
      // @ts-ignore
      top: 0,
      behavior: "smooth"
    });
  }
}
