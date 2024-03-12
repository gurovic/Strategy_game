import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {MainPageComponent} from "./components/__PAGES/main-page/main-page.component";
import {AboutUsComponent} from "./components/__PAGES/about-us/about-us.component";
import {WikiComponent} from "./components/__PAGES/wiki/wiki.component";
import {SandboxComponent} from "./components/__PAGES/sandbox/sandbox.component";
import {ContestsComponent} from "./components/__PAGES/contests/contests.component";
import {ContactUsComponent} from "./components/__PAGES/contact-us/contact-us.component";
import {LoginComponent} from "./components/__PAGES/login/login.component";
import {RegistrationComponent} from "./components/__PAGES/registration/registration.component";

const routes: Routes = [
    {path: '', component: MainPageComponent},
    {path: 'about', component: AboutUsComponent},
    {path: 'wiki', component: WikiComponent},
    {path: 'sandbox', component: SandboxComponent},
    {path: 'contests', component: ContestsComponent},
    // {path: 'contact', component: ContactUsComponent},
    {path: 'login', component: LoginComponent},
    {path: 'register', component: RegistrationComponent},
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule {
}
