import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";

@Component({
    selector: 'app-top-bar',
    templateUrl: './top-bar.component.html',
    styleUrls: ['./top-bar.component.scss']
})
export class TopBarComponent implements OnInit {

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

    open_menu() {
        let menu = document.getElementById('dropdown-menu')!;

        menu.style.display='block';
        setTimeout(()=>{
            menu.style.transform = 'translateY(0)';
        })
    }
    close_menu() {
        let menu = document.getElementById('dropdown-menu')!;
        menu.style.transform = 'translateY(-100%)';
        setTimeout(()=>{
            menu.style.display='none';
        }, 500)
    }
    interact_menu() {
        let menu = document.getElementById('dropdown-menu')!;

        if (menu.style.display == 'none' || menu.style.display=='') this.open_menu();
        else this.close_menu();
    }
}
