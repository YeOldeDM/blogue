from bge import types, logic
from random import randint as rand
from random import choice

S = 4					#Dungeon tile scale
PLAYER_HEIGHT = 2.54		#Height of the player

class Rect:
	#A rectangle used to define a room
	def __init__(self, x, y, w, h):
		self.x1 = x
		self.y1 = y
		self.x2 = x + w
		self.y2 = y + h
		
		self.stairs = False	#to keep up and down stairs from sharing rooms
	def center(self):
		center_x = round((self.x1 + self.x2) / 2)
		center_y = round((self.y1 + self.y2) / 2)
		return (center_x, center_y)
		
	def intersect(self, other):
		return (self.x1 <= other.x2 and self.x2 >= other.x1 and
				self.y1 <= other.y2 and self.y2 >= other.y1)


class Tile:
	def __init__(self, block=None):
		self.block = block
		self.block_index = 0
		self.prop = None
		
		self.explored = False	#has the player set foot on this tile yet?



class Dungeon:
	def __init__(self, sys, width, height):
		self.sys = sys
		self.width = width
		self.height = height
		
		
		self.maps = [self.make_map()]
		self.map = self.maps[0]
		
		self.props = []
		self.items = []
		self.monsters = []
		self.corpses = []
		
		self.generate_map()
		
		
	def make_map(self):
		return [[Tile()
				for y in range(self.height) ]
					for x in range(self.width) ]
	
	def generate_map(self):
		
		#room size and number limits
		ROOM_MAX_SIZE = 5
		ROOM_MIN_SIZE = 3
		MAX_ROOMS = (self.width+self.height)//2
		
		rooms = []
		num_rooms = 0
		#create random rooms, make sure they don't intersect
		mobs = 0
		pots = 0
		for r in range(MAX_ROOMS):
			w = rand(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
			h = rand(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
			
			x = rand(0, self.width - w - 1)
			y = rand(0, self.height - h - 1)
			
			new_room = Rect(x,y,w,h)
			
			failed = False
			for other_room in rooms:
				if new_room.intersect(other_room):
					if rand(1,20) >= 1:
						failed = True
						break
			
			if not failed:
				self.create_room(new_room)
				
				(new_x, new_y) = new_room.center()
				
				if num_rooms == 0:
					#place player here
					center = new_room.center()
					self.sys.player.worldPosition = [center[0]*S, center[1]*S, (PLAYER_HEIGHT/2)+0.05]
				#connect this room with the previous room
				else:
					(prev_x, prev_y) = rooms[num_rooms-1].center()
					
					if rand(0,1) == 1:
						self.create_h_tunnel(prev_x, new_x, prev_y)
						self.create_v_tunnel(prev_y, new_y, new_x)
					else:
						self.create_v_tunnel(prev_y, new_y, prev_x)
						self.create_h_tunnel(prev_x, new_x, new_y)
				
				
				#place random monsters in the room
				monsters = rand(0,(w+h)//1.4)
				for b in range(monsters):
					x = rand(new_room.x1+1, new_room.x2-1)
					y = rand(new_room.y1+1, new_room.y2-1)
					if not self.map[x][y].prop:
						if rand(1,4) == 4:
							self.map[x][y].prop = 'LifePotion'
							pots += 1
						else:
							self.map[x][y].prop = 'Zombie'
							mobs += 1
				
				
				#append the room and continue
				rooms.append(new_room)
				num_rooms += 1
				
		print("Created {} monsters".format(str(mobs)))
		print("Created {} potions".format(str(pots)))
		
		#make stairs
		
		self.find_stairs()
		self.find_stairs(down=False)
		
		#find block indexes
		for y in range(self.height):
			for x in range(self.width):
				if self.map[x][y].block:
					self.map[x][y].block_index = self.find_block_index(x,y)
		
		#blit those blocks!
		self.draw_map()
	
					
	def draw_map(self):
		for y in range(self.height):
			for x in range(self.width):
				self.sys.own.worldPosition = [x*S,y*S,0]
				if self.map[x][y].block:
					index = self.map[x][y].block_index
					try:
						mesh = self.map[x][y].block+str(index)
						tile = logic.getCurrentScene().addObject(mesh,self.sys.own)
						self.map[x][y].block = tile
					except ValueError:
						raise Exception("**********\nStairs at {} {} are reested! \nCorrect block for index {} not found!\n**********".format(x,y,index))
						logic.endGame()
		
				#draw props
				if self.map[x][y].prop:
					p = self.map[x][y].prop
					self.sys.own.worldPosition = [(x*S)+rand(-1,1),(y*S)+rand(-1,1), 2]
					if p == 'LifePotion':
						self.sys.own.worldPosition.z = 0
					prop = logic.getCurrentScene().addObject(p, self.sys.own)
					ori = prop.worldOrientation.to_euler()
					ori.z = rand(0,628)*0.01
					prop.worldOrientation = ori
					if p == 'Zombie':
						self.monsters.append(prop)
					elif p == 'LifePotion':
						self.items.append(prop)
	
	def find_block_index(self, x, y):
		#Look to our neighbors, and define a bitfield?
		index = 0
		if y+1 <= self.height-1:
			if self.map[x][y+1].block:
				index += 1
		if x-1 >= 0:
			if self.map[x-1][y].block:
				index += 8
		
		if y-1 >= 0:
			if self.map[x][y-1].block:
				index += 4
		
		if x+1 <= self.width-1:
			if self.map[x+1][y].block:
				index += 2
		
		return index
		
	def create_room(self, room):
		for x in range(room.x1, room.x2):
			for y in range(room.y1, room.y2):
				self.map[x][y].block = 'dungeon_'
	
	def create_h_tunnel(self, x1, x2, y):
		for x in range(min(x1, x2), max(x1, x2) + 1):
			self.map[x][y].block = 'dungeon_'
	
	def create_v_tunnel(self, y1, y2, x):
		for y in range(min(y1, y2), max(y1, y2) + 1):
			self.map[x][y].block = 'dungeon_'
	
	def isValid(self,x,y):
		if 0 <= x <= self.width-1 and 0 <= y <= self.height-1:
			return True
		return False
		
	def check_neighbors(self, x,y):
		num = 0
		#check cardinal neighbors
		if self.isValid(x,y+1):
			if self.map[x][y+1].block:
				num += 1
		
		if self.isValid(x,y-1):
			if self.map[x][y-1].block:
				num += 1

		if self.isValid(x-1,y):
			if self.map[x-1][y].block:
				num += 1
		
		if self.isValid(x+1,y):
			if self.map[x+1][y].block:
				num += 1
		
		#check diagonals too! Diagonal neighbors = instant fail
		'''					
		if self.isValid(x+1,y+1):
			if self.map[x+1][y+1].block:
				num = 0
		
		if self.isValid(x-1,y+1):
			if self.map[x-1][y+1].block:
				num = 0
		
		if self.isValid(x+1,y-1):
			if self.map[x+1][y-1].block:
				num = 0
		
		if self.isValid(x-1,y-1):
			if self.map[x-1][y-1].block:
				num = 0
		'''				
		return num
		
	
	def find_stairs(self,down=True):
		candidates = []
		for y in range(self.height):
			for x in range(self.width):
				if not self.map[x][y].block:
					go = self.check_neighbors(x,y)
					if go == 1:
						candidates.append((x,y))
		if candidates:
			
			r = choice(candidates)
			print(r)	
			self.create_stairs(r[0],r[1],down)
			print(self.map[r[0]][r[1]].block)
	


	def create_stairs(self, x, y, down=True):
		direction = 'down'
		if not down:
			direction = 'up'
		self.map[x][y].block = 'dungeon_'+direction+'stairs_'
		

