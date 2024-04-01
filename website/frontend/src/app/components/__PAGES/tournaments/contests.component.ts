import {Component, OnInit} from '@angular/core';
import {debug_cards} from "../../../interface/contest_card";
import {TournamentApiService} from "../../../services/api/tournament-api.service";
import {ProfileApiService} from "../../../services/api/profile-api.service";
import {ProfileService} from "../../../services/profile.service";
import {Profile} from "../../../models/profile.model";
import {TournamentModel} from "../../../models/api/tournament.model";

@Component({
    selector: 'app-tournaments',
    templateUrl: './contests.component.html',
    styleUrls: ['./contests.component.scss']
})
export class ContestsComponent implements OnInit {
    public future_cards: TournamentModel[] = [];
    public past_cards: TournamentModel[] = [];
    public user: Profile = {is_registered: false};

    constructor(
        private tournament_service: TournamentApiService,
        private profile_api_service: ProfileApiService,
        private profile_service: ProfileService,
    ) {
    }

    ngOnInit(): void {
        this.user = this.profile_service.user;
        if (!this.user.is_registered)
            this.profile_api_service.get().subscribe(
                resp => {
                    this.profile_service.set_user(resp);
                    this.user = this.profile_service.get_user();

                    this.tournament_service.get().subscribe(
                        resp => {
                            console.log(resp);
                            this.future_cards = resp.future;
                            this.past_cards = resp.past;
                        }
                    );
                },
                error => {
                    this.profile_service.clear();
                    this.user = this.profile_service.get_user();
                },
            );
    }
}
