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

    change_text_forward(id:number, count:number = 100) {
        let text = this.cards[id].about_text;
        let card_text = document.getElementById('card-text-'+id)!;
        if (count >= text.length) {
            card_text.innerText = text;
            this.opened = id;
            return;
        }

        card_text.innerText = text.slice(0,count)+'...';
        setTimeout(()=>{
            this.change_text_forward(id,count+1);
        },(text.length-100)/1000)
    }
    change_text_reverse(id: number, count: number) {
        let text = this.cards[id].about_text;
        let card_text = document.getElementById('card-text-'+id)!;
        card_text.innerText = text.slice(0, count)+'...';

        if (count<=100) {
            this.opened=-1;
            return;
        }

        setTimeout(()=>{
            this.change_text_reverse(id,count-1);
        },(text.length-100)/1000)
    }

    show_more_about_text(card_index: number) {
        let card_bp_id = 'text-part-of-card-'+card_index;
        let card_id = 'card'+card_index;
        if (this.opened != -1) {
            let prev_text_part = document.getElementById('text-part-of-card-'+this.opened)!;
            this.change_text_reverse(this.opened, this.cards[card_index].about_text.length);
            if (this.opened == card_index) return;
        }
        let text_part = document.getElementById(card_bp_id)!;
        let card = document.getElementById(card_id)!;

        this.change_text_forward(card_index);
    }

}
