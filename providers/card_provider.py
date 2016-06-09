from palringo import *

class CardProvider():
 
  def __init__(self, bot, cardQueryFactory):
    self.bot = bot
    self.cardQueryFactory = cardQueryFactory

  # get Card From card_id
  def getCardFromCardID(self, card_id, result_cb):
     self.bot.executeQuery(self.cardQueryFactory.createQueryGetCardFromCardID(card_id, result_cb))

  # get all cards
  def getAllCards(self, card_type, result_cb):
     self.bot.executeQuery(self.cardQueryFactory.createQueryGetAllCards(card_type, result_cb))