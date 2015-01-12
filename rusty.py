import sys
import random
import pygame
class Rusty:
    def __init__(self,location,speed,state):
        pygame.init()
        self.location = location
        self.speed = speed
        self.state = state
        self.stateInAir = "notInAir"
        self.originLocation = []
        self.originLocation.append(location[0])
        self.originLocation.append(location[1])
        
        self.image = pygame.image.load("rusty.png").convert_alpha()
        self.rect = self.image.get_rect()
	self.onBox  = "notOnBox" 
	
    
    def move(self):
        tempy = self.location[1]
        self.location[0]+=(self.rect.width/2)*self.speed[0]
        
        self.location[1]+=(self.rect.height/2)*self.speed[1]
        
    
    def speedLeft(self):
    	if(self.onBox=="notOnBox"):
    	    self.speed[0]-=0.5
    def speedRight(self):
    	if(self.onBox=="notOnBox"):
    	    self.speed[0]+=0.5
    def speedUp(self):
        if(self.speed[1]>-1.0):
            self.speed[1]=-1.0
        
    def speedDown(self):
        if(self.speed[1]<1.0):
            self.speed[1]+=1.0
    def comeToGround(self):
        self.location[1] = self.originLocation[1]
    def collide(self,box):
    	if((box.location[1]<self.location[1]+self.rect.height/2 and box.location[1]>self.location[1]-self.rect.height/2) and (box.location[0]<self.location[0]+self.rect.width/2 and box.location[0]>self.location[0]-self.rect.width/2)):
    		return True
    		
    def actions(self, count,box):
        if(self.state=="jumpup"):
            if(count==0):
            	if(self.onBox=="notOnBox"):
                    self.speed[1] = -1.0
                    self.state="speedtop"
                   
                else:
                    self.state = "jumpdown"
                if(self.stateInAir=="left"):
                    self.speed[0] = -0.5
                if(self.stateInAir=="right"):
                    self.speed[0] = 0.5
               
                    
        if(self.state=="speedtop"):
            if(count==1):
                self.speed[1] = 0
                self.state = "jumpdown"
                if(self.stateInAir=="left"):
                    self.speed[0] = -0.5
                if(self.stateInAir=="right"):
                    self.speed[0] = 0.5
                    
        if(self.state=="jumpdown"):
            if(count==10):
                self.speed[1] = 1.0
                self.state = "dropped"
                if(self.stateInAir=="left"):
                    self.speed[0] = -0.5
                if(self.stateInAir=="right"):
                    self.speed[0] = 0.5
                if(self.onBox=="onBox"):
                    self.speed[0] = 0
                    self.onBox = "notOnBox"
                
        if(self.state=="dropped"):
            
            if(count==11):
                self.speed[1] = 0
                if(self.collide(box) and (box.picked=="dropped" or box.picked=="ground")):
                    self.location[1] = box.location[1]-box.rect.height/2
                    self.onBox = "onBox"
                else:
                    if(self.stateInAir=="left"):
                        self.speed[0] = -0.5
                        self.stateInAir = "notInAir" 
                    if(self.stateInAir=="right"):
                        self.speed[0] = 0.5
                        self.stateInAir = "notInAir" 
               
                self.state = "ground"
             
        self.move()     
        return count+1
        
        
        
