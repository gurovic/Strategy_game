import {Component, OnInit} from '@angular/core';
import {ContestCard, debug_cards} from "../../../interface/contest_card";
import {text} from "d3";

@Component({
    selector: 'app-contests',
    templateUrl: './contests.component.html',
    styleUrls: ['./contests.component.scss']
})
export class ContestsComponent implements OnInit {
    public cards = debug_cards;
    public opened = -1;

    constructor() {
    }

    ngOnInit(): void {
    }

    get_text(text:string): string {
        let result:string = text.slice(0,100) + '...';

        return result;
    }

    show_more_about_text(card_index: number) {
        console.log(this.opened, card_index);
        let card_bp_id = 'text-part-of-card-'+card_index;
        let card_id = 'card'+card_index;
        if (this.opened != -1) {
            let prev_text_part = document.getElementById('text-part-of-card-'+this.opened)!;
            prev_text_part.style.height = 'var(--size)';
            if (this.opened == card_index) { this.opened = -1; return; }
            this.opened = -1;
        }
        let text_part = document.getElementById(card_bp_id)!;
        let card = document.getElementById(card_id)!;
        text_part.style.height = '400px';

        this.opened = card_index;
    }

}
