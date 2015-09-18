from bge import logic, render
from math import pi
from random import randint
from .item import Item

#jar the player's head orientation based on impact force
def head_kick(head, impact):
	r_z = randint(-10,10)*0.01*(impact)
	r_x = randint(-10,10)*0.01*(impact)
	head.parent.applyRotation([0,0,r_z], False)
	head.applyRotation([r_x,0,0], True)



class Thing:
	def __init__(self, own, Name, 
					sprite=None, fighter=None, ai=None,
					item=None, prop=None):
							
		self.own = own
		self.sys = own.scene.objects['System']
		self.Name = Name
		
		self.state = 'idle'
		
		self.sprite = sprite
		
		self.fighter = fighter
		self.ai = ai
		
		self.item = item
		
		self.prop = prop
		
		if self.sprite:		self.sprite.owner = self
		if self.fighter:	self.fighter.owner = self
		if self.ai:			self.ai.owner = self
		if self.item:		self.item.owner = self
		if self.prop:		self.prop.owner = self
		
	def __repr__(self):
		return "THING {} @ x{} y{}".format(self.Name, self.x, self.y)
	
	@property
	def facing(self):
		D = 8	#number of directions desired
		z = self.own.worldOrientation.to_euler().z * (180/pi)
		if z < 0:	z += 360
		facing = round(z / (360/D))
		if facing == D:	facing = 0
		return facing
	
	@property
	def x(self):
		return round(self.own.worldPosition.x/4)
	
	@property
	def y(self):
		return round(self.own.worldPosition.y/4)
	
		
	#I get hit by something
	def get_hit(self, damage, origin=None):
		origin_name = origin.Name
		if origin_name == None:
			origin_name = "A Mysterious Force"
		print("{} is hit by {} for {} damage!".format(self.Name, origin_name, damage))
		self.own['sfx_hit'] = True
		#self.own.applyMovement([0,-(damage),damage*0.5], True)
		if self.fighter:
			self.fighter.hurt(damage, origin)
			if self.ai and self.own['thing'] != 'Player':	#specials for non-player AI
				self.state = 'hurt'	
				self.ai.last_attacker = origin	#become hostile toward our damage source
			
			#extra stuff for player hurting
			elif self.own['thing'] == 'Player':
				head = self.own.children['Head']
				impact = damage / self.fighter.HP
				head_kick(head,impact)
				
	#I get killed by something			
	def kill(self, origin):
		self.sprite.active = False
		self.sprite.current_frame = 0		
		self.item = Item(None)
		self.item.owner = self
		
		self.sprite.action = 'death'
		
		self.sprite.own['frames'] = 12
		self.sprite.own['rate'] = 12
		self.sprite.direction = None
		self.sprite.loop = False
		self.sprite.own['has_face'] = False	#disable direction for death/corpse
		
		self.Name += " Corpse"
		self.fighter = None
		self.AI = None
		
		self.state = 'dead'
		self.sys['sys'].world.monsters.remove(self.own)
		self.sys['sys'].world.corpses.append(self.own)
		self.own.collisionGroup = 2
	
	
	#Special case for player death	
	def player_kill(self, origin):
		T = logic.globalDict['play_time']
		origin_name = origin.Name
		if origin_name == "None":
			origin_name = "Mysterious Force (probably a bug)"
		logic.globalDict['epitaph'] = "Here lies {}, slain by a {} after {}".format(self.Name, origin_name, T)
		logic.sendMessage("PLAYER_DEATH")
