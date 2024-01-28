import {Component, OnInit} from '@angular/core';
import {ContestCard, debug_cards} from "../../../interface/contest_card";

@Component({
    selector: 'app-contests',
    templateUrl: './contests.component.html',
    styleUrls: ['./contests.component.scss']
})
export class ContestsComponent implements OnInit {
    public cards = debug_cards;

    constructor() {
    }

    ngOnInit(): void {
    }

}
