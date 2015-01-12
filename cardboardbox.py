import sys
import random


class Cardboardbox:
	def __init__(self,location,picked):
		self.location = location
		self.picked = picked
		
	def pickup(self,rus):
		
		self.location[0] = rus.location[0]
		self.location[1] = rus.location[1]
		
	def drop(self,rus):
		if(rus.state=="ground"):
			self.location[1] = self.location[1]
		else:
			self.location[1] = self.location[1]+50
	def stayOnGround(self):
		self.location[0] = self.location[0]
		self.location[1] = self.location[1]
