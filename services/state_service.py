
from palringo import *
from cah_bot.game import Game, GameStates

class StateService():
 
  def __init__(self):
    # map of state and actions
    self.stateActions = {
      GameStates.InitGame : self.initGame,
      GameStates.InitRound : self.initNextRound,
      GameStates.InRound : self.inRound,
      GameStates.SubmittingCard : self.whiteCardsSubmitted,
      GameStates.CardSubmitted : self.inCardSubmitted,
      GameStates.SubmittedAllCards : self.submittedAllCards,
      GameStates.InitRoundComplete : self.blackPlayerSelectsWinningCard,
      GameStates.RoundComplete : self.roundComplete,
      GameStates.InitGameComplete : self.initGameComplete
    }

  def initGame(self, game, payload):
    game.initGame(payload)

  def initNextRound(self, game, payload):
    game.initNextRound(payload)

  def inRound(self, game, payload):
    game.inRound(payload)

  def whiteCardsSubmitted(self, game, payload):
    game.whiteCardsSubmitted(payload)

  def inCardSubmitted(self, game, payload):
    game.inCardSubmitted(payload)

  def blackPlayerSelectsWinningCard(self, game, payload):
    game.blackPlayerSelectsWinningCard(payload)

  def submittedAllCards(self, game, payload):
    game.inSubmittedAllCards(payload)

  def roundComplete(self, game, payload):
    game.inRoundCompleted(payload)

  def initGameComplete(self, game, payload):
    game.initGameComplete(payload)


  def processState(self, game, payload):

    if game.gameState == GameStates.Idle:
      return

    # run state action
    self.stateActions[game.gameState](game, payload)
    

