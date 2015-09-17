from bge import logic

class Item:
	def __init__(self,use_effect=None, owned_by=None):
		self.use_effect = use_effect
		self.owned_by = owned_by
		
	def __repr__(self):
		return "ITEM component of {}".format(self.owner)
