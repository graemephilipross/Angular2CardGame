# coding: utf-8
from palringo import Bot, CommandProcessorV2
from palringo.message import types
from palringo.gamepad import gamepadEvent

from cah_bot.container import Container
from cah_bot.emit import Emit
from cah_bot.game import GameStates

SUPPORTED_LANGUAGES = ['en', 'fa', 'de', 'es', 'ar', 'sv', 'tr', 'hi', 'pl', 'nl', 'fr', 'ru', 'pt']

class CahBot(Bot):
  def __init__(self):
    super(CahBot, self).__init__(True)
    self.bot_name = "cah"
    self.supported_languages = SUPPORTED_LANGUAGES
    self.command_processor = dict()
    self.container = None

  def phrasesLoaded(self):

    # initialise ioc container
    try:
      if self.container == None:
        self.container = Container(self)
    except Exception as e:
      print e
      self.log_exception()

    for lang in self.supported_languages:
      self.command_processor[lang] = self.makeCommandProcessor( self, lang )

  # this event fires when a user opens the gamepad
  @gamepadEvent
  def getCurrentGameState(self, subscriber_id, group_id, payload):
    
    try: 

      # get game
      currentGame = self.container.gameService.fetchGameFromGroupID(group_id)
      if currentGame == None:
        return

      if subscriber_id not in [p.sub_id for p in currentGame.players]:
        return

      # send js the users sub id
      def getCurrentGameStateCaptured(sub_id_captured, gameState):

        e = Emit(group_id, subscriber_id, 'playerInit', {'sub_id' : sub_id_captured, 'game_state' : gameState})
        self.container.emitService.addEmitToQueue(e)

      getCurrentGameStateCaptured(subscriber_id, currentGame.gameState)

      # run process method for game state
      self.container.stateService.processState(currentGame, {'sub_id' : subscriber_id})

    except Exception as e:
      print e
      self.log_exception()

  @gamepadEvent
  def initPlayer(self, subscriber_id, group_id, payload):

    try:

      # create or get game 
      currentGame = self.container.gameService.fetchGameFromGroupID(group_id)
      if currentGame == None:
        currentGame = self.container.gameService.createGameFromGroupID(group_id, self.container.cardService, self.container.emitService)

      # add player to player list
      currentGame.addPlayerToGame(subscriber_id, self.container.playerFactory)

      # call state service with payload and game state
      self.container.stateService.processState(currentGame, {})

      # THIS EVENT IS STILL BEING SENT - PREVENT IT SOMEHOW

    except Exception as e:
      print e
      self.log_exception()
    
  #gamepadEvent - round in progress
  @gamepadEvent
  def submitWhiteCard(self, subscriber_id, group_id, payload):

    try:

      # get game
      currentGame = self.container.gameService.fetchGameFromGroupID(group_id)
      if currentGame == None:
        return

      # set game state to round in progress
      currentGame.gameState = GameStates.SubmittingCard

      # call state service with payload and game state
      self.container.stateService.processState(currentGame, {'sub_id' : subscriber_id, 'card_id' : payload['card_id']})

      # THIS EVENT IS STILL BEING SENT - PREVENT IT SOMEHOW

    except Exception as e:
      print e
      self.log_exception()

  #gamepadevent - round complete
  @gamepadEvent
  def winnerSelected(self, subscriber_id, group_id, payload):

    try:

      # get game
      currentGame = self.container.gameService.fetchGameFromGroupID(group_id)
      if currentGame == None:
        return

      # set game state to round complete
      currentGame.gameState = GameStates.InitRoundComplete

      # call state service with payload and game state
      self.container.stateService.processState(currentGame, {'sub_id' : payload['sub_id'], 'card_id' : payload['card_id']})
      
      # game complete? run init game complete state process
      if currentGame.gameState == GameStates.InitGameComplete:
        self.container.stateService.processState(currentGame, {'sub_id' : subscriber_id})

        # remove game
        self.container.gameService.removeGame(group_id)

      # THIS EVENT IS STILL BEING SENT - PREVENT IT SOMEHOW

    except Exception as e:
      print e
      self.log_exception()

  @gamepadEvent
  def initNextRound(self, subscriber_id, group_id, payload):

    try:

      # get game
      currentGame = self.container.gameService.fetchGameFromGroupID(group_id)
      if currentGame == None:
        return

      currentGame.playersSelectNextRound({'sub_id' : subscriber_id})

      # call state service with payload and game state
      self.container.stateService.processState(currentGame, {'sub_id' : subscriber_id})

      # THIS EVENT IS STILL BEING SENT - PREVENT IT SOMEHOW

    except Exception as e:
      print e
      self.log_exception()

  def makeCommandProcessor(self, bot, lang):
    processor = CommandProcessorV2({
      "farming_command_farm": self.sendHelpMessage
    }, self, lang)
    return processor

  def processMessage(self, message):
    try:
      if message.mesg_type != types.PLAIN_TEXT:
        return

      sub = self.getSubscriber(message.source_id)
      if sub.isBot():
        return

      self.lang = self.getLanguage(message)
      if message.to_group:
        self.command_processor[self.lang].process(message)
      else:
        self.sendHelpMessage(None, message)
  
    except:
      self.log_exception()

  def sendHelpMessage(self, args, message):
    try:
      if message.to_group:
        self.sendTextGroupMessage(message.group_id, self.phrases.getPhrase(self.lang, "farming_help_message"))

      else:
        self.sendTextPrivateMessage(message.source_id, self.phrases.getPhrase(self.lang, "farming_help_message"))

    except:
      self.log_exception()

    return True

botclass = CahBot