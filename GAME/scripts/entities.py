#	Factories for creating Entities
#
#
'''
	things Reference:
	
		Later
'''
from .things import Thing, Fighter, BasicMonster, Item, Stairs
from .things import Potion_Heal
from .sprite_wrapper import Sprite

from random import randint as roll

def Player(own):
	f = Fighter(HP=20, power=6, defense=1)
	a = BasicMonster()
	return Thing(own, "Jenkins", fighter=f, ai=a)

def Zombie(own,sprite):
	f = Fighter(HP=roll(10,20), power=6, defense=1)
	a = BasicMonster()
	s = Sprite(sprite, 'zombie', active=True, direction=True, loop=True, action='walk')
	return Thing(own, 'Zombie', sprite=s, fighter=f, ai=a)

def ZombieCorpse(own):
	s = Sprite(own, 'zombie_death', active=True, direction=False, loop=False)
	return Thing(own, 'Zombie Corpse', sprite=s)


def LifePotion(own):
	i = Item(Potion_Heal)
	return Thing(own, "Life Potion", item=i)
	
def StairsDown(own):
	s = Stairs()
	return Thing(own, "Stairs going downward", stairs=s)	
	
def StairsUp(own):
	s = Stairs()
	return Thing(own, "Stairs going upward", stairs=s)
