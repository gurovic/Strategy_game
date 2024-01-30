import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {MainPageComponent} from './components/__PAGES/main-page/main-page.component';
import {TopBarComponent} from './components/top-bar/top-bar.component';
import {AboutUsComponent} from './components/__PAGES/about-us/about-us.component';
import {ContestsComponent} from './components/__PAGES/contests/current/contests.component';
import {SandboxComponent} from './components/__PAGES/sandbox/sandbox.component';
import {WikiComponent} from './components/__PAGES/wiki/wiki.component';
import {ContactUsComponent} from './components/__PAGES/contact-us/contact-us.component';
import {LoginComponent} from './components/__PAGES/login/login.component';
import {BottomBarComponent} from './components/bottom-bar/bottom-bar.component';
import {NgOptimizedImage} from "@angular/common";
import {ArchiveTaskComponent} from './components/__MODELS/archive-task/archive-task.component';
import {RegistrationComponent} from './components/__PAGES/registration/registration.component';
import {LatestCompetitionsComponent} from './components/__PAGES/contests/latest/latest-competitions.component';
import {HttpClient, HttpClientModule} from "@angular/common/http";

@NgModule({
    declarations: [
        AppComponent,
        MainPageComponent,
        TopBarComponent,
        AboutUsComponent,
        ContestsComponent,
        SandboxComponent,
        WikiComponent,
        ContactUsComponent,
        LoginComponent,
        BottomBarComponent,
        ArchiveTaskComponent,
        RegistrationComponent,
        LatestCompetitionsComponent
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        NgOptimizedImage,
        HttpClientModule,
    ],
    providers: [],
    bootstrap: [AppComponent]
})
export class AppModule {
}
