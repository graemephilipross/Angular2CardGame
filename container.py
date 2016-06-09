from palringo import *

from cah_bot.factories.card_query_factory import CardQueryFactory
from cah_bot.providers.card_provider import CardProvider
from cah_bot.factories.card_factory import CardFactory
from cah_bot.providers.player_provider import PlayerProvider
from cah_bot.factories.player_factory import PlayerFactory
from cah_bot.providers.game_provider import GameProvider
from cah_bot.services.game_service import GameService
from cah_bot.services.card_service import CardService
from cah_bot.services.emit_service import EmitService
from cah_bot.services.state_service import StateService

# main container
class Container():
  def __init__(self, bot):
    self.bot = bot

    # initialise card query factory
    self.cardQueryFactory = CardQueryFactory(self.bot)

    # initialise emit service
    self.emitService = EmitService(self.bot)

    # initialise card provider
    self.cardProvider = CardProvider(self.bot, self.cardQueryFactory)

    # initialise card factory
    self.cardFactory = CardFactory(self.bot, self.cardProvider)

    # initialise card service
    self.cardService = CardService(self.cardFactory)

    # initialise player provider
    self.playerProvider = PlayerProvider()

    # initialise player factory
    self.playerFactory = PlayerFactory(self.playerProvider)

    # initialise game provider
    self.gameProvider  = GameProvider()

    # initilaise game service
    self.gameService = GameService(self.gameProvider)

    # initialise state service
    self.stateService = StateService()

