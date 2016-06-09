
from palringo import *

class EmitService():
 
  def __init__(self, bot):
    self.bot = bot

   # create emit
  def addEmitToQueue(self, emit):
    # add to queue and do managment

    # debug
    print emit.data

    # send
    self.bot.sendGamepadEvent(emit.group_id, emit.sub_ids, emit.eventName, emit.data)