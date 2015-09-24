#	Factories for creating Entities
#
#

from .things.fighter import Fighter, PlayerFighter
from .things.ai import BasicMonster	#new name!
from .things.item import Item
from .things.prop import Prop
from .things.thing import Thing

#from .things import Potion_Heal
from .sprite_wrapper import Sprite

from random import randint as roll

def Player(own):
	f = PlayerFighter(level=1, xp=0, 
			strength=10, agility=10, vitality=10, magic=10, 
			HP=50)
	#f = Fighter(HP=100, power=6, defense=1)
	a = BasicMonster()
	return Thing(own, "Jenkins", fighter=f, ai=a)




def Zombie(own,sprite):
	f = Fighter(hitDice=1, damage=(1,10), armor=3)
	a = BasicMonster()
	s = Sprite(sprite, 'zombie', active=True, direction=True, loop=True, action='walk')
	return Thing(own, 'Zombie', sprite=s, fighter=f, ai=a)





def ZombieCorpse(own):
	s = Sprite(own, 'zombie_death', active=True, direction=False, loop=False)
	return Thing(own, 'Zombie Corpse', sprite=s)






def LifePotion(own):
	i = Item()
	return Thing(own, "Life Potion", item=i)
	
	
	
	
	
	
def StairsDown(own):
	p = Prop()
	return Thing(own, "Stairs going downward", prop=p)	
	
	
	
	
	
def StairsUp(own):
	p = Prop()
	return Thing(own, "Stairs going upward", prop=p)
