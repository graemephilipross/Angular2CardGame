
from palringo import *
from cah_bot.card_queries import GetCardFromCardID, GetAllCards

class CardQueryFactory():
  
  def __init__(self, bot):
    self.bot = bot

  def createQueryGetCardFromCardID(self, card_id, result_cb):
    return GetCardFromCardID(self.bot, card_id, result_cb)

  def createQueryGetAllCards(self, card_type, result_cb):
    return GetAllCards(self.bot, card_type, result_cb)