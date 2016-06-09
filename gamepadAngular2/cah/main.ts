import {bootstrap}    from '@angular/platform-browser-dynamic';
import {enableProdMode, provide} from '@angular/core';
import {AppComponent} from './app.component';
import {ROUTER_PROVIDERS} from '@angular/router-deprecated';
import {LocationStrategy, HashLocationStrategy} from '@angular/common';

//enableProdMode();
bootstrap(AppComponent, [
    ROUTER_PROVIDERS,
    provide(LocationStrategy, {useClass: HashLocationStrategy})
]);
