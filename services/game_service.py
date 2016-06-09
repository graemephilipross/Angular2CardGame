
from palringo import *

class GameService():
 
  def __init__(self, game_provider):
    self.gameProvider = game_provider
    self.currentGamesBeingPlayed = {}

  # fetch game - group_id
  def fetchGameFromGroupID(self, group_id):
    game = self.gameProvider.fetchGameFromGroupID(group_id)
    if game != None:
      self.currentGamesBeingPlayed[group_id] = game
    return game
    
  # create game - group_id
  def createGameFromGroupID(self, group_id, cardService, emitService):
    game = self.gameProvider.createGame(group_id, cardService, emitService)
    self.currentGamesBeingPlayed[group_id] = game
    return game

  # delete game - group_id
  def removeGame(self, group_id):
    self.currentGamesBeingPlayed.pop(group_id, None)
    self.gameProvider.removeGame(group_id)