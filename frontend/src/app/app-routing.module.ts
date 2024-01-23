import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {MainPageComponent} from "./components/pages/main-page/main-page.component";
import {AboutUsComponent} from "./components/pages/about-us/about-us.component";
import {WikiComponent} from "./components/pages/wiki/wiki.component";
import {SandboxComponent} from "./components/pages/sandbox/sandbox.component";
import {ContestsComponent} from "./components/pages/contests/contests.component";
import {ContactUsComponent} from "./components/pages/contact-us/contact-us.component";
import {LoginComponent} from "./components/pages/login/login.component";

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
