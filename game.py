
from palringo import *
import random
import threading

from cah_bot.emit import Emit

# game state enum
class GameStates:
  Idle = "idle"
  InitGame = "initgame"
  InitRound = "startround"
  InRound = "inround"
  SubmittingCard = "submittingcard"
  CardSubmitted = "cardsubmitted"
  SubmittedAllCards = "submittedallcards"
  InitRoundComplete = "initroundcomplete"
  RoundComplete = "roundcomplete"
  InitGameComplete = "initgamecomplete"

# game
class Game():
  def __init__(self, group_id, cardService, emitService):
    self.group_id = group_id
    self.gameState = GameStates.Idle
    self.players = []
    # consts
    self.noOfWinningPointsRequired = 4 #7
    self.playerMinimumToInitGame = 3 #3
    # current black player
    self.currentBlackPlayer = None
     # populate cards
    self.whiteCards = cardService.whiteCards
    self.blackCards = cardService.blackCards
    # emit service
    self.emitService = emitService
    # round info
    self.submittedWhiteCards = []
    self.reSubmittedPlayerSubIDs = []
    self.roundWinnerSub_id = None
    # lock
    self.lock = threading.Lock()

  # add player to game
  def addPlayerToGame(self, sub_id, playerFactory):

    self.lock.acquire()
    try:

      if self.gameState != GameStates.Idle:
        return
        
      # check if player already added to game
      if not any(x.sub_id == sub_id for x in self.players):
        # create player 
        player = playerFactory.createPlayer(sub_id)
        # add player to player list
        self.players.append(player)

      # give the js the sub_id
      def addPlayerToGameCaptured(captured_sub_id, gameState):
        e = Emit(self.group_id, sub_id, 'playerInit', {'sub_id' : captured_sub_id, 'game_state' : gameState})
        self.emitService.addEmitToQueue(e)

      addPlayerToGameCaptured(sub_id, self.gameState)

      # can start game?
      if len(self.players) >= self.playerMinimumToInitGame:
         self.gameState = GameStates.InitGame

    finally:
      self.lock.release()

  # remove player from game
  def removePlayerFromGame(sub_id):
    elemIndex = self.players.index(sub_id)
    self.players.pop(elemIndex, None)

  # call on init state
  def initGame(self, payload = None):

    self.lock.acquire()
    try:

      if self.gameState != GameStates.InitGame:
        return

      # set random player as black
      randomBlack = random.randrange(0, len(self.players))
      getBlackPlayer = self.players[randomBlack]
      self.currentBlackPlayer = getBlackPlayer

      # black player - gets a random black card
      randomBlackCard = random.randrange(0, len(self.blackCards))
      self.currentBlackPlayer.blackCard = self.blackCards[randomBlackCard]

      # give each player 10 white cards (hidden on view for black player  - js logic will do this)
      for whitePlayer in self.players:
        # shuffle and select first 10 cards
        random.shuffle(self.whiteCards)
        randomWhiteCards = self.whiteCards[:10]
        whitePlayer.whiteCards = randomWhiteCards

      # emit the data
      # emit players list (black player will have extra blackCard prop)
      def initGameCaptured(players):

        sub_ids = [x.sub_id for x in players]
        e = Emit(self.group_id, sub_ids, 'initRound', {'players' : [p.dump() for p in players]})
        self.emitService.addEmitToQueue(e)

      initGameCaptured(self.players)

      # in round 
      self.gameState = GameStates.InRound

    finally:
      self.lock.release()

  # call on begin round state
  # winning sub id, card_id
  def initNextRound(self, payload = None):

    self.lock.acquire()
    try:

      if self.gameState != GameStates.InitRound:
        return

      # get a random new black card (different from previous)
      newBlackCards = filter(lambda x: self.currentBlackPlayer.blackCard.card_id != x.card_id, self.blackCards)
      randomBlackCard = random.randrange(0, len(newBlackCards))

      # get a random new black player (different from previous)
      previousWhitePlayers = filter(lambda x: self.currentBlackPlayer.sub_id != x.sub_id, self.players)
      randomBlackPlayer = random.randrange(0, len(previousWhitePlayers))

      # clear the current black player
      self.currentBlackPlayer.blackCard = None
    
      # set the new black player
      self.currentBlackPlayer = previousWhitePlayers[randomBlackPlayer]
      self.currentBlackPlayer.blackCard = newBlackCards[randomBlackCard]

      # emit data
      # emit players list (black player will have extra blackCard prop)
      def initNextRoundCaptured(players):

        sub_ids = [x.sub_id for x in players]
        e = Emit(self.group_id, sub_ids, 'initRound', {'players' : [p.dump() for p in players]})
        self.emitService.addEmitToQueue(e)

      initNextRoundCaptured(self.players)

      # in round 
      self.gameState = GameStates.InRound

    finally:
      self.lock.release()

  # call during a round in progress
  def whiteCardsSubmitted(self, payload = None):

    self.lock.acquire()
    try:

      if self.gameState != GameStates.SubmittingCard:
        return

      sub_id = payload['sub_id']
      card_id = payload['card_id']

      # add card to submitted cards
      for card in self.whiteCards:
        if card.card_id == card_id:
            self.submittedWhiteCards.append([sub_id, card])

      self.gameState = GameStates.CardSubmitted

      # if all cards have been submitted (exclude black count)
      # call allWhitCardsSubmitted
      if len(self.submittedWhiteCards) == (len(self.players) - 1):

        def whiteCardsSubmittedCaptured(currentBlackPlayerSub_id, submittedWhiteCards):

          # when all cards are submitted send a private emit to black player
          e = Emit(self.group_id, currentBlackPlayerSub_id, 'submittingAllWhiteCards', {'submittedWhiteCards' : [[w[0], w[1].dump()] for w in submittedWhiteCards]})
          self.emitService.addEmitToQueue(e)

        whiteCardsSubmittedCaptured(self.currentBlackPlayer.sub_id, self.submittedWhiteCards)

        self.gameState = GameStates.SubmittedAllCards

    finally:
      self.lock.release()

  # sub_id and card_id of winning player
  def blackPlayerSelectsWinningCard(self, payload = None):

    self.lock.acquire()
    try:

      if self.gameState != GameStates.InitRoundComplete:
        return

       # clear submittedwhitecards
      self.submittedWhiteCards = []

      sub_id = payload['sub_id']
      card_id = payload['card_id']

      # remove the winners winning white card
      # give them a new white card
      winningPlayer = next((x for x in self.players if x.sub_id == sub_id), None)
      if winningPlayer != None:

        newWhiteCards = [x for x in self.whiteCards if x not in winningPlayer.whiteCards]
        randomNewWhiteCard = random.randrange(0, len(newWhiteCards))
        newWhiteCard = newWhiteCards[randomNewWhiteCard]

        for item in winningPlayer.whiteCards:
          if item.card_id == card_id:
            winningPlayer.whiteCards.remove(item)

        winningPlayer.whiteCards.append(newWhiteCard)

      # calculate score for player (point systemn to be defined later)
      winningPlayer.points += 1

      # if a winner - change state to game complete
      if winningPlayer.points == self.noOfWinningPointsRequired:
        self.gameState = GameStates.InitGameComplete
        return

      def blackPlayerSelectsWinningCardCaptured(captured_sub_id, players):

        # emit init next round event if no one has won
        sub_ids = [x.sub_id for x in players]
        # display all player points and show avatar of winning player
        e = Emit(self.group_id, sub_ids, 'endOfRound', {'players' : [p.dump() for p in players], 'winning_sub_id' : captured_sub_id})
        self.emitService.addEmitToQueue(e)

      blackPlayerSelectsWinningCardCaptured(sub_id, self.players)

      self.roundWinnerSub_id = sub_id
      self.gameState = GameStates.RoundComplete

    finally:
      self.lock.release()

  def playersSelectNextRound(self, payload = None):

    self.lock.acquire()
    try:

      if self.gameState != GameStates.RoundComplete:
        return

      sub_id = payload['sub_id']

      # check if all users have clicked next for the moment
      for player in self.players:
        if player.sub_id == sub_id and sub_id not in self.reSubmittedPlayerSubIDs:
          self.reSubmittedPlayerSubIDs.append(sub_id)
    

      if len(self.players) == len(self.reSubmittedPlayerSubIDs):
        # call init next round
        self.gameState = GameStates.InitRound

        # clear resubmitted players
        self.reSubmittedPlayerSubIDs = []

    finally:
      self.lock.release()
   
  def initGameComplete(self, payload = None):
    def initGameCompleteCaptured(players):
      # send game data
      sub_ids = [x.sub_id for x in players]
      e = Emit(self.group_id, sub_ids, 'initGameComplete', {'players' : [p.dump() for p in players]})
      self.emitService.addEmitToQueue(e)

    initGameCompleteCaptured(self.players)

  def inRound(self, payload = None):
    def inRoundCaptured(sub_id, players):

      # emit round data
      e = Emit(self.group_id, sub_id, 'initRound', {'players' : [p.dump() for p in players]})
      self.emitService.addEmitToQueue(e)

    inRoundCaptured(payload['sub_id'], self.players)
    
  def inCardSubmitted(self, payload = None):
    def inCardSubmittedCaptured(sub_id, players, submittedWhiteCards):

      if sub_id in submittedWhiteCards:
        # card already submitted
        e = Emit(self.group_id, sub_id, 'whiteCardSubmitted', {'players' : [p.dump() for p in players]})
        self.emitService.addEmitToQueue(e)
      else:
        # send in round state
        e = Emit(self.group_id, sub_id, 'initRound', {'players' : [p.dump() for p in players]})
        self.emitService.addEmitToQueue(e)

    inCardSubmittedCaptured(payload['sub_id'], self.players, self.submittedWhiteCards)

  def inSubmittedAllCards(self, payload = None):
    def inSubmittedAllCardsCaptured(sub_id, currentBlackPlayerSubID, submittedWhiteCards, players):
      
      if sub_id == currentBlackPlayerSubID:
        # black player
        e = Emit(self.group_id, sub_id, 'allWhiteCardsSubmitted', {'submittedWhiteCards' : [[w[0], w[1].dump()] for w in submittedWhiteCards]})
        self.emitService.addEmitToQueue(e)
      else:
        # white player
        e = Emit(self.group_id, sub_id, 'whiteCardSubmitted', {'players' : [p.dump() for p in players]})
        self.emitService.addEmitToQueue(e)

    inSubmittedAllCardsCaptured(payload['sub_id'], self.currentBlackPlayer.sub_id, self.submittedWhiteCards, self.players)
    
  def inRoundCompleted(self, payload = None):
    def inRoundCompletedCaptured(sub_id, players, roundWinnerSub_id):

      # display all player points and show avatar of winning player
      e = Emit(self.group_id, sub_id, 'endOfRound', {'players' : [p.dump() for p in players], 'winning_sub_id' : roundWinnerSub_id})
      self.emitService.addEmitToQueue(e)

    inRoundCompletedCaptured(payload['sub_id'], self.players, self.roundWinnerSub_id)
