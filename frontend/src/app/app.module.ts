import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MainPageComponent } from './components/main-page/main-page.component';
import { TopBarComponent } from './components/top-bar/top-bar.component';
import { AboutUsComponent } from './components/about-us/about-us.component';
import { ContestsComponent } from './components/contests/contests.component';
import { SandboxComponent } from './components/sandbox/sandbox.component';
import { WikiComponent } from './components/wiki/wiki.component';
import { ContactUsComponent } from './components/contact-us/contact-us.component';
import { LoginComponent } from './components/login/login.component';
import { BottomBarComponent } from './components/bottom-bar/bottom-bar.component';

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
    BottomBarComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
