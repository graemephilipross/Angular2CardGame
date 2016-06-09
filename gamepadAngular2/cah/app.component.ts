import {Component, OnInit, NgZone} from '@angular/core';
import {SubscriberService} from './subscriber.service';
import {RouteConfig, RouteDefinition, Router, ROUTER_DIRECTIVES } from '@angular/router-deprecated';
import {MenuViewComponent, RoundViewComponent, CardsSubmittedComponent, EndOfRoundComponent, GameCompleteComponent} from './cah.components';

declare var window: any;

@Component({
    selector: 'cah',
    template:`<router-outlet></router-outlet>`,
    providers: [SubscriberService],
    directives: [ROUTER_DIRECTIVES]
})
@RouteConfig([ {path:'/menu-view',         name: 'MenuView',     component: MenuViewComponent, useAsDefault: true},
            {path:'/round-view',        name: 'RoundView',       component: RoundViewComponent},
            {path:'/cards-submitted',   name: 'CardsSubmitted',  component: CardsSubmittedComponent},
            {path:'/end-of-round',      name: 'EndOfRound',      component: EndOfRoundComponent},
            {path:'/game-complete',     name: 'GameComplete',    component: GameCompleteComponent}])

export class AppComponent implements OnInit {

    private stateActions: any;

    constructor(private _router: Router,
                private _ngZone: NgZone){}

    ngOnInit() {
        window.routeComponent = {component: this};

        this.stateActions = {
            "initRound" : function(eventData) {  this._router.navigate( ['RoundView', { eventData: eventData }] );  },
            "submittingAllWhiteCards" : function(eventData) { this._router.navigate( ['CardsSubmitted', { eventData: eventData }] );   },
            "allWhiteCardsSubmitted" : function(eventData) {  this._router.navigate( ['CardsSubmitted', { eventData: eventData }] );   },
            "endOfRound" : function(eventData) { this._router.navigate( ['EndOfRound', { eventData: eventData }] );  },
            "initGameComplete" : function(eventData) { this._router.navigate( ['GameComplete', { eventData: eventData }] ); },
            "whiteCardSubmitted" : function(eventData) { this._router.navigate( ['RoundView', { eventData: eventData, 'whiteCardHasBeenSubmitted' : true }] ); }
        };
    }

    changeState(action:string, eventData:any): void {
        this._ngZone.run(() => {
            this.stateActions[action](eventData);
        });
    }
}