
from palringo import *

class CardService():
 
  def __init__(self, card_factory):
    self.cardFactory = card_factory
    self.blackCards = []
    self.whiteCards = []

    # populate cards
    self.cardFactory.fetchAllCards(self.successGotAllCards, self.failGotAllCards)


  def successGotAllCards(self, allCards):

    if allCards != []:
      self.populateBlackCards(allCards)
      self.populateWhiteCards(allCards)
    
  def failGotAllCards(self):
    pass

  # populate white cards
  def populateWhiteCards(self, allCards):
    self.whiteCards = filter(lambda x: x.card_type == 1, allCards)

  # populate black cards
  def populateBlackCards(self, allCards):
    self.blackCards = filter(lambda x: x.card_type == 2, allCards)

