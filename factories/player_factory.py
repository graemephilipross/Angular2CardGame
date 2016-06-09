
from palringo import *

class PlayerFactory():
 
  def __init__(self, player_provider):
    self.playerProvider = player_provider

  # create a Player
  def createPlayer(self, sub_id):
    return self.playerProvider.createPlayer(sub_id)

  # create a Player White
  def createPlayerWhite(self, sub_id):
    return self.playerProvider.createPlayerWhite(sub_id)
     
  # create a Player Black
  def createPlayerBlack(self, sub_id):
      return self.playerProvider.createPlayerBlack(sub_id)