import {Component, AfterViewInit, HostListener, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {Profile} from "../../../models/profile.model";
import {ProfileApiService} from "../../../services/api/profile-api.service";
import {ProfileService} from "../../../services/profile.service";

@Component({
    selector: 'app-main-page',
    templateUrl: './main-page.component.html',
    styleUrls: ['./main-page.component.scss']
})
export class MainPageComponent implements AfterViewInit, OnInit {
    public user: Profile = {is_registered: false};

    constructor(
        private router: Router,
        private route: ActivatedRoute,
        private profile_api_service: ProfileApiService,
    ) {
    }

    ngOnInit(): void {
        this.profile_api_service.get().subscribe(
            resp => {
                this.user = resp;
                this.user.is_registered = true;
            },
            error => {
                this.user.is_registered = false;
            },
        )
    }

    ngAfterViewInit(): void {
    }

    go(link: string) {
        this.router.navigate([link]);
    }
}
