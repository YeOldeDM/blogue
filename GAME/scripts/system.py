from bge import logic
from .map import Dungeon

class Clock:
	def __init__(self):
		self.raw_time = 0
		
	@property
	def play_time(self):
		T = self.raw_time//60
		
		seconds = T
		minutes = T//60
		hours = minutes//60
		
		seconds -= minutes*60
		minutes -= hours*60
		'''
		if seconds < 10:
			seconds = "0"+str(seconds)
		if minutes < 10:
			seconds = "0"+str(minutes)
		if hours < 10:
			seconds = "0"+str(hours)
		'''
		return "{}h {}m {}s".format(hours,minutes,seconds)

class System:	
	def __init__(self, own, WIDTH, HEIGHT):
		self.own = own
		self.width = WIDTH
		self.height = HEIGHT
		
		self.player = logic.getCurrentScene().objects['Player']
		
		self.world = Dungeon(self, self.width, self.height)
		
		self.clock = Clock()
	
	def clock_tick(self):
		self.clock.raw_time += 1
		logic.globalDict['play_time'] = self.clock.play_time
		
		
	def monster_AI(self):
		for prop in self.world.monsters:
			if prop.invalid:
				self.world.monsters.remove(prop)
			elif 'ent' in prop:
				if prop['ent'].ai and prop != self.player:
					if prop.getDistanceTo(self.player) <= 35.0 and prop['ent'].ai.los_ray(self.player):
						prop['ent'].ai.think()

		
	def get_minimap(self):
		grid = [["X" for x in range(7)] for y in range(7)]
		
		cx = self.player['ent'].x
		cy = self.player['ent'].y
		if not self.map[cx][cy].explored:
			self.map[cx][cy].explored = True
			
		for y in range(7):
			for x in range(7):
				mx = (cx - 3)+x
				my = (cy - 3)+y
				if 0 <= mx <= self.width-1 and 0 <= my <= self.height-1:
					if self.map[mx][my].block:
						grid[x][y] = "O"
						if self.map[mx][my].explored:
							grid[x][y] = "E"
		logic.globalDict['minimap_grid'] = grid
		
		
		
