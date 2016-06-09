
from palringo import *
import types

# emit 
class Emit():
  
  def __init__(self, group_id, sub_ids, eventName, data):
    self.group_id = group_id
    self.sub_ids = sub_ids
    self.eventName = eventName
    self.data = data