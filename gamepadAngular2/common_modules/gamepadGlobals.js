/**
 * Created by Graeme on 04/02/2016.
 */

// Globally Exposed Functions

// Main Game Object
this.Game = this.Game || {};

// JS Interface 'On' Listener
function parseCommandResponse(eventName, state) {
    Game.OnEventHandlers.events[eventName](state);
}

/**
 * Browser Testing Functions
 */
// JS Interface 'Emit' Listener
function emit() {};
