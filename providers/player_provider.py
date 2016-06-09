
from palringo import *
from cah_bot.player import Player, PlayerWhite, PlayerBlack

class PlayerProvider():
 
  def __init__(self):
    pass

  # create a Player
  def createPlayer(self, sub_id):
    return Player(sub_id)

  # create a Player White
  def createPlayerWhite(self, sub_id):
    return PlayerWhite(sub_id)
     

  # create a Player Black
  def createPlayerBlack(self, sub_id):
    return PlayerBlack(sub_id)