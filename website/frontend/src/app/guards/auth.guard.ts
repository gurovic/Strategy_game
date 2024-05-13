import {Injectable} from '@angular/core';
import {ActivatedRouteSnapshot, CanActivate, Route, Router, RouterStateSnapshot, UrlTree} from '@angular/router';
import {Observable} from 'rxjs';
import {LoginApiService} from "../services/api/login-api.service";
import {ProfileApiService} from "../services/api/profile-api.service";
import { firstValueFrom} from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class AuthGuard implements CanActivate {
    constructor(
        private router: Router,
        private login_service: LoginApiService,
        private profile_service: ProfileApiService,
    ) {
    }

    async canActivate(
        route: ActivatedRouteSnapshot,
        state: RouterStateSnapshot): Promise<boolean | UrlTree> {

        try {
            let result = await firstValueFrom(this.profile_service.get());
            return true;
        } catch (e: any) {
            return false;
        }
    }

}
