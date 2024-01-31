import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";

@Component({
    selector: 'app-bottom-bar',
    templateUrl: './bottom-bar.component.html',
    styleUrls: ['./bottom-bar.component.scss']
})
export class BottomBarComponent implements OnInit {

    constructor(
        private router: Router,
        private route: ActivatedRoute,
    ) {
    }

    ngOnInit(): void {
    }

    go_link(link: string): void {
        this.router.navigate([link]);
        window.scrollTo({
            // @ts-ignore
            top: 0,
            behavior: "smooth"
        });
    }

}
