import asyncdb
from palringo import *

class GetCardFromCardID(asyncdb.Query):
    def __init__(self, bot, card_id, result_cb):
      try:
        self.bot               = bot
        self.result_function   = result_cb
        self.query           = """SELECT card_type, 
                                         message 
                                  FROM sb_bots.cah_card 
                                  WHERE card_id = %s """ % card_id
        self.cache_update_type = asyncdb.CACHE_NONE
        self.query_type        = asyncdb.SELECT
        self.use_cache = False
        self.update_cache_expiration = False
      except:
        bot.log_exception()

class GetAllCards(asyncdb.Query):
    def __init__(self, bot, card_type, result_cb):
      try:
        self.bot               = bot
        self.result_function   = result_cb

        if (card_type != None):
          self.query = "SELECT card_id, card_type, message FROM sb_bots.cah_card WHERE card_type = %d" % (card_type)
        else:
          self.query = "SELECT card_id, card_type, message FROM sb_bots.cah_card"

        self.cache_update_type = asyncdb.CACHE_NONE
        self.query_type        = asyncdb.SELECT
        self.use_cache = False
        self.update_cache_expiration = False
      except:
        bot.log_exception()