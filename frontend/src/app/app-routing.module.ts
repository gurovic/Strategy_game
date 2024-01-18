import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {MainPageComponent} from "./components/main-page/main-page.component";
import {AboutUsComponent} from "./components/about-us/about-us.component";
import {WikiComponent} from "./components/wiki/wiki.component";
import {SandboxComponent} from "./components/sandbox/sandbox.component";
import {ContestsComponent} from "./components/contests/contests.component";
import {ContactUsComponent} from "./components/contact-us/contact-us.component";
import {LoginComponent} from "./components/login/login.component";

const routes: Routes = [
    {path: '', component: MainPageComponent},
    {path: 'about', component: AboutUsComponent},
    {path: 'wiki', component: WikiComponent},
    {path: 'sandbox', component: SandboxComponent},
    {path: 'contests', component: ContestsComponent},
    {path: 'contact', component: ContactUsComponent},
    {path: 'login', component: LoginComponent}
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule {
}
