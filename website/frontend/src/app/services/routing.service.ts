import { Injectable } from '@angular/core';
import {Router} from "@angular/router";

@Injectable({
  providedIn: 'root'
})
export class RoutingService {

  constructor(
      private router: Router,
  ) { }

  navigate(link: string) {
    this.router.navigate([link]).then();
  }
}
