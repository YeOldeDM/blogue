from bge import logic
from random import randint
from mathutils import Vector

class BasicMonster:
	
	def __init__(self):
		self.target = None
		self.ai_timer = 0
		
		self.state = 'idle'
		
		self.last_attacker = None	#The last creature to hurt me
		
		self.frame_track = None
		
	def __repr__(self):
		return "AI component of {}".format(self.owner)
	
	
	#General thinking loop
	def think(self):
		if self.state == 'dead':
			return
		
		#sprite information
		if self.state == 'idle':
			self.owner.sprite.action = 'walk'
			self.owner.sprite.own['rate'] = 10
		elif self.state == 'attack':
			self.owner.sprite.action = 'strike'
			self.owner.sprite.own['rate'] = 8
			
		#print("The {} growls!").format(self.owner.Name)
		"""My standard AI cycle"""	
		if self.target:
			if self.target.invalid:
				self.target = None
			if self.target == self.owner.own:
				self.target = None
		
		#make the player the target if all else fails
		if not self.target:
			self.target = self.owner.sys['sys'].player

		self.face(self.target)
		if self.owner.own.getDistanceTo(self.target) > 1.5 and self.state == 'idle':
			if self.owner.sprite.current_frame != self.frame_track:
				self.advance()
				self.frame_track = self.owner.sprite.current_frame
	
		if self.state == 'attack':
			self.ai_timer += 1
			if self.ai_timer >= self.owner.fighter.attack_rate:
				if self.owner.own.getDistanceTo(self.target) <= self.owner.fighter.attack_range:
					self.fight()

				self.ai_timer = 0
				self.state = 'idle'

			
		elif self.state == 'hurt':
			self.ai_timer += 1
			if self.ai_timer >= 30:
				self.ai_timer = 0
				self.state = 'idle'
				self.target = self.last_attacker
	
	


	#Hook to fighter's attack method				
	def fight(self):
		self.owner.fighter.attack()

							
	def advance(self, mod=1.0):
		"""Move our object forward at our movement rate, multiplied by mod"""
		obstacle = self.sight_ray(1.25)
		if not obstacle:
			
			new_pos = self.owner.own.worldPosition + (self.owner.own.localOrientation.col[1]*(self.owner.fighter.move_speed*mod))
			self.owner.own.worldPosition = new_pos
		else:
			if randint(1,10) <= 3 and 'ent' in obstacle:
				if hasattr(obstacle,'fighter'):	#only go for fighters
					self.target = obstacle
					self.state = 'attack'
				
	def face(self, target):
		"""Turn my object to face its target"""
		v = self.owner.own.getVectTo(target)		#get the vector to the target
		rate = self.owner.fighter.turn_rate
		self.owner.own.alignAxisToVect(v[1],1,rate)	#steer toward the vector
		self.owner.own.alignAxisToVect([0,0,1],2,1)	#keep local +Z snapped to global +Z
		if v[0] <= self.owner.fighter.attack_range:
			if self.state != 'hurt':
				self.state = 'attack'

	def los_ray(self, other):
		#check for line of sight to the other
		ray = self.owner.own.rayCast(other, self.owner.own, 0, 'wall',0,1,0)
		for ob in ray:
			if ob != None:
				return False
		#render.drawLine(self.owner.own.worldPosition, other.worldPosition, [1,1,0])
		return True

	def sight_ray(self, distance):
		"""check for objects directly in front of me, up to distance"""
		vec = (self.owner.own.localOrientation.col[1]*100)+Vector(self.owner.own.worldPosition)
		#render.drawLine(self.owner.own.worldPosition, vec, [1,0,0])	#test line
		wall = self.owner.own.rayCast(vec,self.owner.own, distance,'wall',0,1,0)
		thing = self.owner.own.rayCast(vec,self.owner.own, distance,'thing', 0,1,0)
		if thing[0]:
			if thing[0].state != 'dead':
				return thing[0]
		if wall[0]:
			return wall[0]
