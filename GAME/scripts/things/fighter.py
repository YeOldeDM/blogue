from bge import logic
from random import randint


class Fighter:
	def __init__(self, HP, power, defense):
		self.maxHP = HP
		self.HP = HP
		self.power = power
		self.defense  = defense
		
		self.turn_rate = 0.08
		self.move_speed = 0.3
		self.attack_range = 3.0
		self.attack_rate = 60
		self.attack_counter = self.attack_rate
		
		self.target = None

	def __repr__(self):
		return "FIGHTER component of {}".format(self.owner)
			
	def hurt(self, damage, origin=None):
		if origin == None:
			origin = self.owner
		self.HP -= damage
		
		if self.HP <= 0:
			#self.owner.state = 'dead'
			print("R.I.P.   {} has died at the hands of {}".format(self.owner.Name, origin.Name))
			#self.owner.sys['sys'].props.remove(self.owner.own)
			if self.owner.own['thing'] != 'Player':
				self.owner.kill(origin)
			elif self.owner.own['thing'] == 'Player':
				self.owner.player_kill(origin)
			
		elif self.HP >= self.maxHP:	self.HP = self.maxHP
		if self.owner.own['thing'] == 'Player':
			value = self.HP / self.maxHP
			logic.sendMessage('update_player_hp', str(value))
		print("{}/{} HP remaining for {}".format(self.HP, self.maxHP, self.owner.Name))
			

	def attack(self):
		d = self.attack_range
		ray = self.owner.ai.sight_ray(d)

		if ray and 'ent' in ray and not ray['ent'].prop:
			ray['ent'].get_hit(self.owner, self.power)
			brush = self.owner.own.scene.objects['System']
			brush.worldPosition = ray.worldPosition
			brush.worldPosition.z += 1.0
			
			#impact blood spray
			emitter = self.owner.own.scene.addObject('Blood Spray', brush, 2)
			emitter['impact'] = self.power
		else:
			print("{} swings at the air!".format(self.owner.Name))