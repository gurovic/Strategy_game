import {AfterViewInit, Component, OnInit} from '@angular/core';
import {Member, OurTeamService} from "../../../services/our-team.service";

@Component({
  selector: 'app-about-us',
  templateUrl: './about-us.component.html',
  styleUrls: ['./about-us.component.scss']
})
export class AboutUsComponent implements OnInit,AfterViewInit {
  public members: Member[] = [];

  constructor(
      private members_service: OurTeamService,
  ) { }

  ngOnInit(): void {
    this.members = this.members_service.members;
  }

  ngAfterViewInit(): void {
    //========== making scrolling cards ===============
    const our_team_images_observer = new IntersectionObserver((entries) => {
      console.log(1);
      entries.forEach((entry) => {
        let new_class_name = 'image-show';
        if (entry.isIntersecting)
          entry.target.classList.add(new_class_name);
        else
          entry.target.classList.remove(new_class_name);
      });
    });
    const hiddenOurTeamImages = document.querySelectorAll('.image-hidden');
    hiddenOurTeamImages.forEach((el) => our_team_images_observer.observe(el));
  }

}
