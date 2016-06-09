
from palringo import *

# players 
class Player():
  def __init__(self, sub_id):
    self.sub_id = sub_id
    # all player types get white cards
    self.whiteCards = []
    self.points = 0
    self.blackCard = None

  def dump(self):
    return {
      'sub_id': self.sub_id,
      'whiteCards': [w.dump() for w in self.whiteCards],
      'points': self.points,
      'blackCard':  self.blackCard.dump() if self.blackCard != None else None
    }

 # not used
class PlayerBlack(Player):
  
  def __init__(self, sub_id):
    super(PlayerBlack, self).__init__(sub_id)
    self.blackCard = None

  # not used
class PlayerWhite(Player):
  
  def __init__(self, sub_id):
    super(PlayerWhite, self).__init__(sub_id)
