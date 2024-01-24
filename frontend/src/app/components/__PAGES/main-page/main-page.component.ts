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
  public svg_filenames = [
    'assets/logos_for_main_page/csharp.svg',
    'assets/logos_for_main_page/c++.svg',
    'assets/logos_for_main_page/c.svg',
    'assets/logos_for_main_page/go.svg',
    'assets/logos_for_main_page/java.svg',
    'assets/logos_for_main_page/js.svg',
    'assets/logos_for_main_page/kotlin.svg',
    'assets/logos_for_main_page/python.svg',
    'assets/logos_for_main_page/rust.svg',
    'assets/logos_for_main_page/ts.svg',
  ]
  public user: Profile = {};

  constructor(
    public router: Router,
    private route: ActivatedRoute,
    private profile_service: ProfileService,
  ) {
  }

  ngAfterViewInit(): void {
    this.user = this.profile_service.get_user();
    if (this.user.registered) this.router.navigate(['contests']);
    ///////////////////// observers ///// /////////
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        let class_name = 'show';
        if (entry.isIntersecting)
          entry.target.classList.add(class_name);
        else
          entry.target.classList.remove(class_name);
      });
    });
    const cards_observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        let class_name = 'little-card__show';
        if (entry.isIntersecting)
          entry.target.classList.add(class_name);
        else
          entry.target.classList.remove(class_name);
      });
    });

    const hiddenElements = document.querySelectorAll('.hidden');
    const hiddenCards = document.querySelectorAll('.little-card__hide');
    hiddenElements.forEach((el) => observer.observe(el));
    hiddenCards.forEach((el) => cards_observer.observe(el));
  }

  getRandomInt(max: number): number {
    return Math.floor(Math.random() * max);
  }

  generate_01_text_line() {
    let result = "";
    for (let i = 0; i < 200; i++) {
      if (this.getRandomInt(2) == 0) result += "0";
      else result += "1";
    }
    // this.cdr.detectChanges();
    return result;
  }

  go(link: string) {
    this.router.navigate([link]);
  }
}
