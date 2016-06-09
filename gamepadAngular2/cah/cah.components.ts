/**
 * Created by Graeme on 4/5/2016.
 */

import {Component, OnInit, NgZone} from '@angular/core';
import {SubscriberService} from './subscriber.service';
//import {} from '@angular/router-deprecated';
import {RouteParams, Router} from '@angular/router-deprecated';
import * as _ from 'underscore';

declare var window: any;
declare var emit: (gameState: string, eventData: any) => void;

@Component({

    template:`
            <div id="menu-view">
                <div class="title">
                    <div class="titleText">
                        Palringo Against Humanity
                    </div>
                </div>
                <div class="actions">
                    <button id="initPlayer" (click)="addPlayer()" [disabled]="sub_id != null">{{message}}</button>
                </div>
            </div>
            `,
})
export class MenuViewComponent implements OnInit {

    private sub_id: number;
    private game_state: any;
    private message: string = "Add Me To Game";

    constructor(private _ngZone: NgZone,
                private _subscriberService: SubscriberService){}

    ngOnInit(): void {
        window.menuComponent = {component: this};
        emit("getCurrentGameState", {});
    }

    addPlayer(): void {
        emit("initPlayer", {});
        this.message = "Waiting For Other Players...";
    }

    playerInit(eventData: any): void {
        this._ngZone.run(() => {
            this.sub_id = eventData.sub_id;
            this.game_state = eventData.game_state;
            this._subscriberService.setSubID(this.sub_id);

            console.log("sub_id = " + this.sub_id + " game_state = " + this.game_state);
        });
    }
}

@Component({
    selector: 'round-view',
    template:`
            <div id="round-view">

                <!-- black player view -->
                <div *ngIf="isBlackPlayer == true">
                    <p>Black Player</p>
                    <p><strong>Question: </strong>{{ blackCard.message }}</p>
                    <p><i>...Waiting for players to submit</i></p>
                </div>

                <!-- white player view -->
                <div *ngIf="isBlackPlayer == false">
                    <p>White Player</p>
                    <p><strong>Your Question: </strong>{{ blackCard.message }}</p>

                    <!-- pre card submitted -->
                    <div *ngIf="selectedWhiteCardSubmitted == false">
                        <label  *ngFor="#card of player.whiteCards">
                            <input type="radio" name="whiteCard" [(ngModel)]="selectedWhiteCard.index" value="card.card_id" />{{card.message}}
                        </label>
                        <button (click)="submitCard()">Submit Card</button>
                    </div>

                    <!-- after card submitted -->
                    <div *ngIf="selectedWhiteCardSubmitted == true">
                        <p><strong>Card Submitted</strong></p>
                        <p><i>{{submitSuccessfulMessage}}</i></p>
                    </div>

                </div>

            </div>
            `,
})
export class RoundViewComponent implements OnInit {

    private sub_id: number;
    private player: any;
    private isBlackPlayer: boolean = false;
    private blackCard: any = null;
    private selectedWhiteCard: { index: number } = { index: null };
    private selectedWhiteCardSubmitted: boolean = false;
    private submitSuccessfulMessage: string;

    constructor(private _ngZone: NgZone,
                private _routeParams: RouteParams,
                private _subscriberService: SubscriberService){}

    ngOnInit(): void {
        window.roundComponent = {component: this};
        this.sub_id = this._subscriberService.getSubID();

        let whiteCardHasBeenSubmitted: any = this._routeParams.get('whiteCardHasBeenSubmitted');
        if (whiteCardHasBeenSubmitted) {
            this.selectedWhiteCardSubmitted = true;
            this.submitSuccessfulMessage = "Waiting on response from player...";
        }

        let eventData: any = this._routeParams.get('eventData');
        let blackPlayer: any = _.find(eventData.players, (player: any) => { return player.blackCard != null });
        this.blackCard = blackPlayer.blackCard;

        this.player = _.find(eventData.players, (player: any) => { return player.sub_id = this.sub_id });

        if (blackPlayer.sub_id = this.player.sub_id)
            this.isBlackPlayer = true;

        // debug
        console.log(this.blackCard);
        console.log(this.player);
        console.log(this.isBlackPlayer);
    }

    submitCard(): void {
        if (this.selectedWhiteCard.index == null)
            return;
        this.selectedWhiteCardSubmitted = true;
        emit("submitWhiteCard", {"card_id" : this.selectedWhiteCard.index});
    }

    whiteCardSubmitted(eventData: any): void {
        this._ngZone.run(() => {
            this.submitSuccessfulMessage = "Waiting on response from player...";
        });
    }

}

@Component({
    selector: 'cards-submitted-view',
    template:`
            <div id="cards-submitted-view">
                <p>Black Player</p>
                <label *ngFor="#card of submittedWhiteCards">
                    <input type="radio" name="whiteCard" [(ngModel)]="selectedWhiteCard.index" value="[card[0],card[1].card_id]" />{{card[1].message}}
                </label>
                <button (click)="submitCard()">Submit Winning Card</button>
            </div>
            `,
})
export class CardsSubmittedComponent implements OnInit {

    private sub_id: number;
    private submittedWhiteCards: any;
    private selectedWhiteCard: { index: number } = { index: null };

    constructor(private _subscriberService: SubscriberService,
                private _routeParams: RouteParams){}

    ngOnInit(): void {
        let eventData: any = this._routeParams.get('eventData');

        this.sub_id = this._subscriberService.getSubID();
        this.submittedWhiteCards = eventData.submittedWhiteCards;

        //debug
        console.log(eventData);
    }

    submitCard():void {
        if (this.selectedWhiteCard.index == null)
            return;

        let winning_sub_id = this.selectedWhiteCard.index[0],
            winning_card_id = this.selectedWhiteCard.index[1];

        console.log("selected sub_id: " + winning_sub_id + " card_id: " + winning_card_id);
        emit("winnerSelected", {"sub_id": winning_sub_id, "card_id" : winning_card_id});
    }
}

@Component({
    selector: 'round-ended',
    template:`
            <div id="round-ended-view">
                <p><strong>Winning Player: {{winning_sub_id}}</strong></p>

                <ul *ngFor="#player of players">
                    <li><b>Player:</b> {{player.sub_id}} - <b>Points:</b> {{player.points}}</li>
                </ul>

                <button (click)="nextRound()" [disabled]="nextRoundSelected">Go To Next Round</button>
            </div>
            `,
})
export class EndOfRoundComponent implements OnInit {

    private sub_id: number;
    private winning_sub_id: number;
    private players: any;
    private nextRoundSelected:boolean = false;

    constructor(private _subscriberService: SubscriberService,
                private _routeParams: RouteParams){}

    ngOnInit(): void {
        let eventData: any = this._routeParams.get('eventData');

        this.sub_id = this._subscriberService.getSubID();
        this.winning_sub_id = eventData.winning_sub_id;
        this.players = eventData.players;

        //debug
        console.log(eventData);
    }

    nextRound():void {
        emit("initNextRound", {});
        this.nextRoundSelected = true;
    }
}

@Component({
    selector: 'game-complete',
    template:`
            <div id="game-complete-view">
                <ul *ngFor="#player of players">
                    <li><b>Player:</b> {{player.sub_id}} - <b>Points:</b> {{player.points}}</li>
                </ul>
            </div>
            `,
})
export class GameCompleteComponent implements OnInit {

    private sub_id: number;
    private players: any;

    constructor(private _subscriberService: SubscriberService,
                private _routeParams: RouteParams){}

    ngOnInit(): void {
        let eventData: any = this._routeParams.get('eventData');

        this.sub_id = this._subscriberService.getSubID();
        this.players = eventData.players;

        //debug
        console.log(eventData);
    }
}