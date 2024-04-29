import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {MainPageComponent} from './components/__PAGES/main-page/main-page.component';
import {TopBarComponent} from './components/top-bar/top-bar.component';
import {AboutUsComponent} from './components/__PAGES/about-us/about-us.component';
import {ContestsComponent} from './components/__PAGES/tournaments/contests.component';
import {SandboxComponent} from './components/__PAGES/sandbox/sandbox.component';
import {WikiComponent} from './components/__PAGES/wiki/wiki.component';
import {ContactUsComponent} from './components/__PAGES/contact-us/contact-us.component';
import {LoginComponent} from './components/__PAGES/login/login.component';
import {BottomBarComponent} from './components/bottom-bar/bottom-bar.component';
import {NgOptimizedImage} from "@angular/common";
import {ArchiveTaskComponent} from './components/__MODELS/archive-task/archive-task.component';
import {RegistrationComponent} from './components/__PAGES/registration/registration.component';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {HttpClientModule, HttpClientXsrfModule} from "@angular/common/http";
import { ProfileComponent } from './components/__PAGES/profile/profile.component';
import { UploadGameComponent } from './components/__PAGES/upload-game/upload-game.component';

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
        ProfileComponent,
        UploadGameComponent
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        NgOptimizedImage,
        FormsModule,
        HttpClientModule,
        HttpClientXsrfModule.withOptions({
            cookieName: 'csrftoken',
            headerName: 'X-CSRFToken',
        }),
        ReactiveFormsModule,
    ],
    providers: [],
    bootstrap: [AppComponent]
})
export class AppModule {
}
