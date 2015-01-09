import sys
import random
class Rusty:
	def __init__(self,location,speed,state):
		self.location = location
		self.speed = speed
		self.state = state
		self.originLocation = []
		self.originLocation.append(location[0])
		self.originLocation.append(location[1])
		self.alreadyPressed = 0
		
		
	def move(self):
		tempy = self.location[1]
		self.location[0]+=2*self.speed[0]
		self.location[1]+=10*self.speed[1]
		
		
	def changeState(self,state):
		self.state = state
	
		
	def speedLeft(self):
		self.speed[0]-=1
	def speedRight(self):
		self.speed[0]+=1
	def speedUp(self):
		self.speed[1]=-1
		
	def speedDown(self):
		self.speed[1]+=1
	def comeToGround(self):
		self.location[1] = self.originLocation[1]
		#self.speed[1] -=1
		
