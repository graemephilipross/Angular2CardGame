

from palringo import *
from cah_bot.game import Game 

 # this provider stores games in memory
class GameProvider():
 
  def __init__(self):
    # all games being played
    # key: group_id 
    self.games = {}

  # fetch game from group id
  def fetchGameFromGroupID(self, group_id):
    return self.games.get(group_id)
    
  # create game - group_id
  def createGame(self, group_id, cardService, emitService):
    # create game
    groupGame = Game(group_id, cardService, emitService)
    # add game to games being played
    self.games[group_id] = groupGame
    return groupGame

  # delete game
  def removeGame(self, group_id):
    self.games.pop(group_id, None)
