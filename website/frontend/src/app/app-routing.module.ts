import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {MainPageComponent} from "./components/__PAGES/main-page/main-page.component";
import {AboutUsComponent} from "./components/__PAGES/about-us/about-us.component";
import {WikiComponent} from "./components/__PAGES/wiki/wiki.component";
import {SandboxComponent} from "./components/__PAGES/sandbox/sandbox.component";
import {ContestsComponent} from "./components/__PAGES/tournaments/contests.component";
import {LoginComponent} from "./components/__PAGES/login/login.component";
import {RegistrationComponent} from "./components/__PAGES/registration/registration.component";
import {ProfileComponent} from "./components/__PAGES/profile/profile.component";
import {
    TournamentUploadSolutionComponent
} from "./components/__PAGES/tournament-upload-solution/tournament-upload-solution.component";
import {TournamentResultComponent} from "./components/__PAGES/tournament-result/tournament-result.component";
import {UploadGameComponent} from "./components/__PAGES/upload-game/upload-game.component";
import {CreateNewComponent} from "./components/__PAGES/create-new/create-new.component";
import {AuthGuard} from "./guards/auth.guard";

const routes: Routes = [
    {path: '', component: MainPageComponent},
    {path: 'about', component: AboutUsComponent},

    {path: 'login', component: LoginComponent},
    {path: 'register', component: RegistrationComponent},
    {path: 'profile', component: ProfileComponent, canActivate: [AuthGuard]},

    {path: 'tournaments', component: ContestsComponent, canActivate: [AuthGuard]},
    {path: 'tournament/upload/:tournament-id', component: TournamentUploadSolutionComponent, canActivate: [AuthGuard]},
    {path: 'tournament/:tournamentId/results', component: TournamentResultComponent, canActivate: [AuthGuard]},
    {path: 'game/upload', component: UploadGameComponent, canActivate: [AuthGuard]},
    {path: 'create', component: CreateNewComponent, canActivate: [AuthGuard]},
    {path: '**', redirectTo: '', pathMatch: 'full'},
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule {
}
