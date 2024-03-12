import {Component, AfterViewInit, HostListener} from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {Profile} from "../../../interface/profile";
import {ProfileService} from "../../../services/profile.service";

@Component({
  selector: 'app-background_svgs',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.scss']
})
export class MainPageComponent implements AfterViewInit {

  constructor(
    public router: Router,
    private route: ActivatedRoute,
  ) {
  }

  ngAfterViewInit(): void {
  }

  go(link: string) {
    this.router.navigate([link]);
  }
}
