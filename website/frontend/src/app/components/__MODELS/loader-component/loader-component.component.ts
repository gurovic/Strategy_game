import {Component, OnInit} from '@angular/core';

@Component({
    selector: 'app-loader-component',
    templateUrl: './loader-component.component.html',
    styleUrls: ['./loader-component.component.scss']
})
export class LoaderComponentComponent implements OnInit {

    constructor() {
    }

    ngOnInit(): void {
    }

    static Show() {
        const loader = document.getElementById('loader-container')!;
        loader.style.display = 'flex';
        setTimeout(() => {
            loader.style.opacity = '1';
        });
    }

    static Hide() {
        const loader = document.getElementById('loader-container')!;
        loader.style.opacity = '0';
        setTimeout(() => {
            loader.style.display = 'none';
        }, 300);
    }

}
