
from palringo import *
from cah_bot.cards import Card

class CardFactory():

  def __init__(self, bot, cardProvider):
    self.bot = bot
    self.cardProvider = cardProvider

  # Need a good promise library! :( Too many callbacks
  def fetchAllCards(self, onCompletion, onFail):
    
    # result closure - create cards
    def createCards(result, query):

      # empty list of cards
      allCards = []
      try:
        if result.has_key('error'):
           self.bot.log('Cah_bot DB error: %s' % str(result['error']))
      
        elif len(result):
        
          for row in result['rows']:
              card_id = int(row[0])
              card_type = int(row[1])
              card_message = str(row[2])

              #create card
              card = Card(card_id, card_type, card_message)
              # add to list
              allCards.append(card)

        # complete callback
        onCompletion(allCards)

      except:
        self.bot.log_exception()
        # fail callback
        onFail()

    # get all cards - card_type, callback
    self.cardProvider.getAllCards(None, createCards)
 