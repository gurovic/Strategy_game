import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {ProfileApiService} from "../../services/api/profile-api.service";
import {ProfileService} from "../../services/profile.service";
import {Profile} from "../../models/profile.model";

@Component({
    selector: 'app-top-bar', templateUrl: './top-bar.component.html', styleUrls: ['./top-bar.component.scss']
})
export class TopBarComponent implements OnInit {
    public user: Profile = {is_registered: false};

    constructor(
        private router: Router,
        private route: ActivatedRoute,
        private profile_api_service: ProfileApiService,
        private profile_service: ProfileService,
    ) {
    }

    ngOnInit(): void {
        this.user = this.profile_service.get_user();
        if (!this.user.is_registered)
            this.profile_api_service.get().subscribe(
                resp => {
                    this.profile_service.set_user(resp);
                    this.user = this.profile_service.get_user();
                },
                error => {
                    this.profile_service.clear();
                    this.user = this.profile_service.get_user();
                },
            )
    }

    go_link(link: string): void {
        this.close_menu();
        this.router.navigate([link]);
        window.scrollTo({
            // @ts-ignore
            top: 0, behavior: "smooth"
        });
    }

    open_menu() {
        let menu = document.getElementById('dropdown-menu')!;

        // @ts-ignore
        document.getElementById('moving-rect')!.style.x = '0px';
        document.getElementById('moving-rect')!.style.width = '36px';
        document.getElementById('menu-icon')!.style.transform = 'rotate(90deg)';

        menu.style.display = 'block';
        setTimeout(() => {
            menu.style.transform = 'translateY(0)';
        })
    }

    close_menu() {
        let menu = document.getElementById('dropdown-menu')!;

        // @ts-ignore
        document.getElementById('moving-rect')!.style.x = '12.6486';
        document.getElementById('moving-rect')!.style.width = '23.3514';
        document.getElementById('menu-icon')!.style.transform = '';

        menu.style.transform = 'translateY(-100%)';
        setTimeout(() => {
            menu.style.display = 'none';
        }, 500)
    }

    interact_menu() {
        let menu = document.getElementById('dropdown-menu')!;

        if (menu.style.display == 'none' || menu.style.display == '') this.open_menu(); else this.close_menu();
    }
}
