import {AfterViewInit, Component, OnInit, ViewChild} from '@angular/core';
import {TournamentModel} from "../../../models/api/tournament.model";
import {TournamentApiService} from "../../../services/api/tournament-api.service";
import {ActivatedRoute, Router} from "@angular/router";
import {GameModel} from "../../../models/api/game.model";
import {GameApiService} from "../../../services/api/game-api.service";
import {Profile} from "../../../models/profile.model";
import {ProfileApiService} from "../../../services/api/profile-api.service";

@Component({
    selector: 'app-tournament-upload-solution',
    templateUrl: './tournament-upload-solution.component.html',
    styleUrls: ['./tournament-upload-solution.component.scss']
})
export class TournamentUploadSolutionComponent implements OnInit, AfterViewInit {
    @ViewChild('rules_container') public rules_container_element: any;
    @ViewChild('name_container') public name_container_element: any;
    @ViewChild('solution_input') public solution_input: any;
    public profile: Profile = {is_registered: false};
    public tournament: TournamentModel = {};
    public game: GameModel = {};
    public solution: any;
    public language: any = 'c++';
    public filename: any;
    public solution_upload_progress?: number;

    constructor(
        private tournament_service: TournamentApiService,
        private game_service: GameApiService,
        private profile_service: ProfileApiService,
        private route: ActivatedRoute,
        private router: Router,
    ) {
    }

    ngOnInit(): void {
        this.GetProfile();
        this.GetTournament();
    }

    ngAfterViewInit() {
        this.rules_container_element = this.rules_container_element.nativeElement;
        this.name_container_element = this.name_container_element.nativeElement;
    }

    ChangeFile() {
        let file_reader = new FileReader();
        file_reader.readAsText(this.solution_input.nativeElement.files[0]);
        this.filename = this.solution_input.nativeElement.files[0].name;

        file_reader.onload = () => { this.solution = file_reader.result; }
        file_reader.onprogress = (e:any) => { this.solution_upload_progress = e.loaded / e.total * 100; }
        file_reader.onloadend = () => { this.solution_upload_progress = undefined; }
        setTimeout(() => {})
    }

    GetProfile() {
        this.profile_service.get().subscribe(
            resp => {
                this.profile = resp;
                this.profile.is_registered = true;
            }, error => {
                this.profile.is_registered = false;
                this.router.navigate(['login']).then();
            },
        )
    }

    GetTournament() {
        const id = Number(this.route.snapshot.paramMap.get('tournament-id'));
        this.tournament_service.get_by_id(id).subscribe(
            resp => {
                this.tournament = JSON.parse(resp.tournament)[0].fields;
                this.tournament.id = JSON.parse(resp.tournament)[0].pk;

                this.game_service.get_by_id(this.tournament.game!).subscribe(
                    resp => {
                        this.game = resp.game;
                        this.game.rules = this.game.rules?.replace('\n', '<br>')
                        for (let i = 0; i < this.game.rules?.length!; i++)
                            if (this.game.rules![i] === '\n')
                                this.game.rules = this.game.rules!.slice(0, i) + '<br>' + this.game.rules!.slice(i + 1, this.game.rules?.length);
                        this.rules_container_element.innerHTML = this.game.rules;
                        this.name_container_element.innerHTML = this.game.name;
                    },
                )
            }, error => {
                alert('error: wrong tournament id');
                this.router.navigate(['']).then();
            }
        )
    }

    SendSolutionFile() {
        if (this.solution === undefined) {
            return;
        }

        let formData = new FormData()
        formData.append('strategy', this.solution_input.nativeElement.files[0]);

        this.tournament_service.upload_solution(formData, this.profile.id!, this.tournament.id!).subscribe(
            resp => {
                console.log(resp);
            }, error => {
                console.log(error);
            }
        )
    }
}
