from palringo import *

# card type enum
# enum matches card.card_type 
class CardType:
  white = 1
  black = 2

# card 
class Card():
  
  def __init__(self, card_id, card_type = CardType.white, message = ""):
    self.card_id = card_id
    self.card_type = card_type
    self.message = message

  def dump(self):
    return {
      'card_id': self.card_id,
      'card_type': self.card_type,
      'message': self.message
    }