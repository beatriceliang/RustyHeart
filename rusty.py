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
        
    '''if not on box, move normally otherwise state changes to "jumpFromBox"'''
    def speedLeft(self):
    	if(self.onBox=="notOnBox"):
    	    self.speed[0]-=0.5
    	else:
            self.state = "jumpFromBox"
            
    '''if not on box, move normally otherwise state changes to "jumpFromBox"'''
    def speedRight(self):
    	if(self.onBox=="notOnBox"):
    	    self.speed[0]+=0.5
    	else:
    	    self.state = "jumpFromBox"
    	    
    def speedUp(self):
        if(self.speed[1]>-1.0):
            self.speed[1]=-1.0
        
    def speedDown(self):
        if(self.speed[1]<1.0):
            self.speed[1]+=1.0
            
    '''returns true if box is close enough to rusty.needed so that we can determine if rusty is falling
    on top of the box'''
    def collide(self,box):
    	if((box.location[1]<self.location[1]+self.rect.height/2 and box.location[1]>self.location[1]-self.rect.height/2) and (box.location[0]<self.location[0]+self.rect.width/2 and box.location[0]>self.location[0]-self.rect.width/2)):
    		return True
    		
    def actions(self, count,countbox,box):
    	print self.state
    	if(self.onBox == "onBox" and self.state=="jumpup"):
            self.state = "jumpFromBox"
    	#countbox is a count related to jumping from the bos
    	if(self.state=="jumpFromBox" and countbox>5):
    	    countbox = 0
    	
        if(self.state=="jumpup" or self.state == "jumpFromBox"):
            if(count==0 or countbox==0):
            	if(self.onBox=="notOnBox"): #jump normally if not on box
                    self.speed[1] = -1.0
                    self.state="speedtop"
                elif (self.state == "jumpFromBox"): #else skip one step in the state machine for jumping
                    self.state = "jumpdown"         #directly go to "jumpdown" step
                    
                    
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
            if(count==10 or countbox==4):
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
            
            if(count==11 or countbox==5):
                self.speed[1] = 0
                
                #determine if rusty should land on top of a box. if it does land
                #change the onBox field to "onBox"
                if(self.collide(box) and (box.picked=="dropped" or box.picked=="ground")):
                    self.location[1] = box.location[1]-box.rect.height/2
                    self.onBox = "onBox"   
                
                #otherwise land on the ground normally
                else:
                    if(self.stateInAir=="left"):
                        self.speed[0] = -0.5
                        self.stateInAir = "notInAir" 
                    if(self.stateInAir=="right"):
                        self.speed[0] = 0.5
                        self.stateInAir = "notInAir" 
               
                self.state = "ground"
             
        self.move()     
        return [count+1,countbox+1]
        
        
        
