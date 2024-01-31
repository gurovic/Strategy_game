import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {MainPageComponent} from "./components/__PAGES/main-page/main-page.component";
import {AboutUsComponent} from "./components/__PAGES/about-us/about-us.component";
import {WikiComponent} from "./components/__PAGES/wiki/wiki.component";
import {SandboxComponent} from "./components/__PAGES/sandbox/sandbox-container/sandbox.component";
import {ContestsComponent} from "./components/__PAGES/contests/current/contests.component";
import {ContactUsComponent} from "./components/__PAGES/contact-us/contact-us.component";
import {LoginComponent} from "./components/__PAGES/login/login.component";
import {LatestCompetitionsComponent} from "./components/__PAGES/contests/latest/latest-competitions.component";
import {RegistrationComponent} from "./components/__PAGES/registration/registration.component";
import {ConstestViewerComponent} from "./components/__PAGES/contests/constest/constest-viewer.component";
import {TaskViewerComponent} from "./components/__PAGES/sandbox/task/task-viewer.component";

const routes: Routes = [
    {path: '', component: MainPageComponent},
    {path: 'about', component: AboutUsComponent},
    {path: 'wiki', component: WikiComponent},
    {path: 'sandbox/container', component: SandboxComponent},
    {path: 'sandbox/task/:id', component: TaskViewerComponent},
    {path: 'contests/current', component: ContestsComponent},
    {path: 'contests/latest', component: LatestCompetitionsComponent},
    {path: 'contests/contest/:id', component: ConstestViewerComponent},
    {path: 'login', component: LoginComponent},
    {path: 'register', component: RegistrationComponent},
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule {
}
