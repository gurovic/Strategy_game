import { Component, OnInit } from '@angular/core';
import {RegisterApiService} from "../../../services/api/register.service";
import {UserRegister} from "../../../models/api/user-register.model";
import {Router} from "@angular/router";

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.scss']
})
export class RegistrationComponent implements OnInit {
  public user: UserRegister = {username: '', password1: '', email: '' , password2: ''};

  constructor(
      public register_service: RegisterApiService,
      private router: Router,
  ) { }

  ngOnInit(): void {
  }

  register() {
    this.register_service.create(this.user).subscribe(
        resp => { console.log(resp) },
        error => { console.log(error) },
    )
  }

  go_link(link:string) {
    this.router.navigate([link]);
  }

}
