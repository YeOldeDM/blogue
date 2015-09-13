'''
Sprite objects should have the following properties defined:
(int) "frames": the number of frames in the animation cycle
(int) "rate": The number of real frames the animation lasts (60=1 sec. at 60fps)
(int) "hit_frame": (optional) the frame in which the Sprite triggers an event (like a weapon/monster attack)
'''
from random import randint

from bge import logic


class Sprite:
	def __init__(self, own, Name, active=True, direction=False, loop=False, action=None):
		self.own = own
		self.Name = Name
		self.loop = loop	#if true, animation runs on a loop. Otherwise, it runs as a one-shot
		self.timer = 0
		self.current_frame = 0
		self.active = active
		
		self.direction = direction	#If not None, add a direction to the frame
		self.action = action	#if not None, action is added to mesh string to provide multiple animation cycles. 'walk', 'attack', 'death', 'leg-hump', etc
		#Naming conventions for animation frame meshes is 'N_A_D_F' where:
			#N = Name of the object ("Goblin")
			#A = Name of action(if present) ("Attack")
			#D = Direction facing of the sprite (-3 to 4)
			#F = The frame number (4), first frame must be 0.
			#That mesh would be named "Goblin_Attack_-1_4"
			#Only the first and last values are required. A and D are optional.
	
	#start/resume an animation
	def start(self):
		if not self.active:
			self.active = True
	
	#(experimental) stop/pause an animation
	def stop(self):
		if self.active:
			self.active = False
			self.timer = 0
			self.current_frame = 0
	

	#sets the mesh based on the NADF formula		
	def set_mesh(self,frame=None):
		N = self.Name + '_'
		A = ''
		D = ''
		F = str(self.current_frame)
		if frame != None:
			F = str(frame)
			
		if self.action != None:
			A = self.action + '_'
		if self.direction == True:
			D = self.own['face'] + '_'
		self.own.replaceMesh(N+A+D+F)
	
	
	#the frame-by-frame management of animation			
	def animate(self):
		if 'paused' in logic.globalDict:
			if not logic.globalDict['paused']:
				if 'rate' in self.own:
					if self.active:
						self.timer += 1
						if self.timer >= self.own['rate']:
							if not self.loop:
								self.stop()
								self.set_mesh()
							else:
								self.timer = 0

						period = self.timer / self.own['rate'] * 10
						self.current_frame = min(self.own['frames']-1, round(period * (self.own['frames']/10)))
						self.set_mesh()

