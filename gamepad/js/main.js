/**
 * Created by Graeme on 04/02/2016.
 */

(function() {

    "use strict";

    /**
     * On Event Handlers
     */
    var OnEventHandlers = (function() {

        function changeState(currentContrl, state, eventData) {
            var injector = currentContrl.injector();
            var stateService = injector.get('StateService');
            stateService.changeState(state , eventData);
        }

        var events = {
            //"eventString" : function(state) { callback }
            "getCurrentGameState": function (eventData) { console.log("getCurrentGameState event response");},
            "initPlayer": function (eventData) { console.log("initPlayer event response");},
            "winnerSelected": function (eventData) { console.log("winnerSelected event response");},
            "initNextRound": function (eventData) { console.log("initNextRound event response");},

            "playerInit" : function(eventData) { angular.element($('#menu-view')).scope().playerInit(eventData); },
            "initRound"  : function(eventData) { changeState(angular.element($('#state-control')), "initRound", eventData); },
            "submitWhiteCard": function (eventData) { angular.element($('#round-view')).scope().whiteCardSubmitted(eventData);},
            "whiteCardSubmitted": function (eventData) { changeState(angular.element($('#state-control')), "whiteCardSubmitted", eventData); },
            "submittingAllWhiteCards": function(eventData) { changeState(angular.element($('#round-view')), "submittingAllWhiteCards", eventData);},
            "allWhiteCardsSubmitted": function (eventData) { changeState(angular.element($('#state-control')), "allWhiteCardsSubmitted", eventData); },
            "endOfRound": function(eventData) { changeState(angular.element($('#state-control')), "endOfRound", eventData); },
            "initGameComplete": function(eventData) { changeState(angular.element($('#state-control')), "initGameComplete", eventData); }
        };

        return {
            events : events
        };

    })();

    Game.OnEventHandlers = OnEventHandlers;

})();

(function() {

    "use strict";

    /**
     * Module Initialisation, Set up DI container
     */

    // initialise game module, inject ui-router, translation provider
    var gamePad = angular.module('cah', ['ui.router', 'gamepadTranslationProvider']);
    gamePad.controller('StateController',['$scope', '$state', '$stateParams', 'StateService',  StateController]);
    gamePad.controller('MenuController',['$scope', '$state', '$stateParams',  MenuController]);
    gamePad.controller('RoundController',['$scope', '$state', '$stateParams',  RoundController]);
    gamePad.controller('CardsSubmitted',['$scope', '$state', '$stateParams',  CardsSubmitted]);
    gamePad.controller('RoundEnded',['$scope', '$state', '$stateParams',  RoundEnded]);
    gamePad.controller('GameComplete',['$scope', '$state', '$stateParams',  GameComplete]);

    /**
     * Service
     */

    gamePad.factory('StateService', function($state) {

        var _sub_id = null;

        var _stateActions = {
            "initRound" : function(eventData) {  $state.go('roundView', {'eventData' : eventData}) },
            "submittingAllWhiteCards" : function(eventData) {  $state.go('cardsSubmitted', {'eventData' : eventData}) },
            "allWhiteCardsSubmitted" : function(eventData) {  $state.go('cardsSubmitted', {'eventData' : eventData}) },
            "endOfRound" : function(eventData) { $state.go('endOfRound', {'eventData' : eventData}) },
            "initGameComplete" : function(eventData) { $state.go('gameComplete', {'eventData' : eventData}) },
            "whiteCardSubmitted" : function(eventData) { $state.go('roundView', {'eventData' : eventData, 'whiteCardHasBeenSubmitted' : true}) }
        };

        function changeState(action, eventData) {
            _stateActions[action](eventData);
        }

        function setSubID(sub_id) {
            _sub_id = sub_id;
        }

        function getSubID() {
            return _sub_id;
        }

        return {
            changeState: changeState,
            setSubID: setSubID,
            getSubID: getSubID
        };
    });

    /**
     * Routes
     */

    // set up routes, inject state provider and route provider
    gamePad.config(function($stateProvider, $urlRouterProvider) {

        // default to Menu view
        $urlRouterProvider.otherwise("/MenuView");

        // Menu View
        $stateProvider
            .state('MenuView', {
                url: "/MenuView",
                templateUrl: "templates/MenuView.html",
                controller: MenuController
            });

        // round
        $stateProvider
            .state('roundView', {
                url: "/roundView",
                templateUrl: "templates/roundView.html",
                params: {'eventData' : null, 'whiteCardHasBeenSubmitted' : null},
                controller: RoundController
            });

        // all white cards submitted
        $stateProvider
            .state('cardsSubmitted', {
                url: "/cardsSubmitted",
                templateUrl: "templates/cardsSubmitted.html",
                params: {'eventData' : null},
                controller: CardsSubmitted
            });

        // round ended
        $stateProvider
            .state('endOfRound', {
                url: "/endOfRound",
                templateUrl: "templates/roundEnded.html",
                params: {'eventData' : null},
                controller: RoundEnded
            });

        // game complete
        $stateProvider
            .state('gameComplete', {
                url: "/gameComplete",
                templateUrl: "templates/gameComplete.html",
                params: {'eventData' : null},
                controller: GameComplete
            });
    });

    /**
     * Controllers
     * @param {type} $scope
     * @returns {undefined}
     */

    function StateController($scope, $state, $stateParams, StateService) {

        // This Ctrls Parent scope allows inner ctrls access to StateService
        $scope.StateService = StateService;
    }

    function MenuController($scope, $state, $stateParams) {

        $scope.sub_id = null;
        $scope.game_state = null;
        $scope.message = "Add Me To Game";

        $scope.playerInit = function (eventData) {
            $scope.$apply(function () {
                $scope.sub_id = eventData.sub_id;
                $scope.game_state = eventData.game_state;
                $scope.StateService.setSubID($scope.sub_id);
                
                console.log("sub_id = " + $scope.sub_id + " game_state = " + $scope.game_state);
            });
        };

        $scope.addPlayer = function() {
            emit("initPlayer", {});
            $scope.message = "Waiting For Other Players...";
        };

        emit("getCurrentGameState", {});
    }

    function RoundController($scope, $state, $stateParams) {

        $scope.sub_id = $scope.StateService.getSubID();
        $scope.player = null;
        $scope.isBlackPlayer = false;
        $scope.blackCard = null;
        $scope.selectedWhiteCard = { index: null };
        $scope.selectedWhiteCardSubmitted = false;

        $scope.submitCard = function() {
            if ($scope.selectedWhiteCard.index == null)
                return;
            $scope.selectedWhiteCardSubmitted = true;
            emit("submitWhiteCard", {"card_id" : $scope.selectedWhiteCard.index});
        };

        $scope.whiteCardSubmitted = function(eventData) {
            $scope.$apply(function () {
                $scope.submitSuccessfulMessage = "Waiting on response from player...";
            });
        };

        // has the card already been submitted?
        if ($stateParams.whiteCardHasBeenSubmitted) {
            $scope.selectedWhiteCardSubmitted = true;
            $scope.submitSuccessfulMessage = "Waiting on response from player...";
        }

        // get black card
        var blackPlayer = _.find($stateParams.eventData.players, function(player) {
            return player.blackCard != null;
        });
        $scope.blackCard = blackPlayer.blackCard;

        // get this player
        $scope.player = _.find($stateParams.eventData.players, function(player){
            return player.sub_id == $scope.sub_id;
        });

        // set is Black Player
        if (blackPlayer.sub_id == $scope.player.sub_id) {
            $scope.isBlackPlayer = true;
        }

        // debug
        console.log($scope.blackCard);
        console.log($scope.player);
        console.log($scope.isBlackPlayer);
    }

    function CardsSubmitted($scope, $state, $stateParams) {

        $scope.sub_id = $scope.StateService.getSubID();
        $scope.submittedWhiteCards = $stateParams.eventData.submittedWhiteCards;
        $scope.selectedWhiteCard = { index: null };

        $scope.submitCard = function() {
            if ($scope.selectedWhiteCard.index == null)
                return;

            var winning_sub_id = $scope.selectedWhiteCard.index[0],
                winning_card_id = $scope.selectedWhiteCard.index[1];

            console.log("selected sub_id: " + winning_sub_id + " card_id: " + winning_card_id);

            emit("winnerSelected", {"sub_id": winning_sub_id, "card_id" : winning_card_id});
        };

        // debug
        console.log($stateParams.eventData);
    }

    function RoundEnded($scope, $state, $stateParams) {

        $scope.sub_id = $scope.StateService.getSubID();
        $scope.winning_sub_id = $stateParams.eventData.winning_sub_id;
        $scope.players = $stateParams.eventData.players;
        $scope.nextRoundSelected = false;

        $scope.nextRound = function() {
            emit("initNextRound", {});
            $scope.nextRoundSelected = true;
        };

        // debug
        console.log($stateParams.eventData);
    }

    function GameComplete($scope, $state, $stateParams) {

        $scope.sub_id = $scope.StateService.getSubID();
        $scope.players = $stateParams.eventData.players;

        // debug
        console.log($stateParams.eventData);
    }

})();

