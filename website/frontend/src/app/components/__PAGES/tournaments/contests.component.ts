import {Component, OnInit, ViewChild} from '@angular/core';
import {debug_cards} from "../../../interface/contest_card";
import {TournamentApiService} from "../../../services/api/tournament-api.service";
import {ProfileApiService} from "../../../services/api/profile-api.service";
import {Profile} from "../../../models/profile.model";
import {TournamentModel} from "../../../models/api/tournament.model";
import {Router} from "@angular/router";
import {LoaderComponentComponent} from "../../__MODELS/loader-component/loader-component.component";

@Component({
    selector: 'app-tournaments',
    templateUrl: './contests.component.html',
    styleUrls: ['./contests.component.scss']
})
export class ContestsComponent implements OnInit {
    public need_close_loader_callbacks_count = 1;
    private have_close_loader_callbacks_count = 0;
    public future_cards: TournamentModel[] = [{}];
    public past_cards: TournamentModel[] = [{}];
    public user: Profile = {is_registered: false};

    constructor(
        private tournament_service: TournamentApiService,
        private profile_api_service: ProfileApiService,
        public router: Router,
    ) {
    }

    CloseLoaderComponent() {
        this.have_close_loader_callbacks_count++;
        if (this.have_close_loader_callbacks_count >= this.need_close_loader_callbacks_count)
            LoaderComponentComponent.Hide();
    }

    ngOnInit(): void {
        LoaderComponentComponent.Show();
        this.profile_api_service.get().subscribe(
            resp => {
                this.user = resp;
                this.user.is_registered = true;

                this.tournament_service.get().subscribe(
                    resp => {
                        this.future_cards = resp.future;
                        this.past_cards = resp.past;
                        this.need_close_loader_callbacks_count += this.future_cards.length;
                        this.CloseLoaderComponent();
                        for (let i = 0; i < this.future_cards.length; ++i) {
                            this.tournament_service.CheckIfUserRegistered(this.future_cards[i].id!, this.user.id!).subscribe(
                                resp => {
                                    if (resp.ok == 'ok')
                                        this.future_cards[i].is_registered = true;
                                    else
                                        this.future_cards[i].is_registered = false;
                                    this.CloseLoaderComponent();
                                }
                            );
                        }
                    }
                );
            },
            error => {
                LoaderComponentComponent.Hide();
                this.router.navigate(['login']).then();
            },
        );
    }

    RegisterToTournament(id: number) {
        LoaderComponentComponent.Show();
        this.tournament_service.RegisterToTournament(id, this.user.id!).subscribe(
            resp => {
                if (resp.status == 'denied registration') alert('registration_denied');
                else {
                    for (let i = 0; i < this.future_cards.length; i++)
                        if (this.future_cards[i].id == id) this.future_cards[i].is_registered = true;
                }
                LoaderComponentComponent.Hide();
            }
        );
    }

    navigate(link: string) {
        this.router.navigate([link]).then();
    }
}
