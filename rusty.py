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
    
    def move(self):
        tempy = self.location[1]
        self.location[0]+=10*self.speed[0]
        
        self.location[1]+=50*self.speed[1]
        
    
                
    def speedLeft(self):
        self.speed[0]-=1
    def speedRight(self):
        self.speed[0]+=1
    def speedUp(self):
        if(self.speed[1]>-1):
            self.speed[1]=-1
        
    def speedDown(self):
        if(self.speed[1]<1):
            self.speed[1]+=1
    def comeToGround(self):
        self.location[1] = self.originLocation[1]
        
    def actions(self, count):
        if(self.state=="jumpup"):
            if(count==0):
                self.speed[1] = -1
                self.state="speedtop"
                if(self.stateInAir=="left"):
                    self.speed[0] = -1
                if(self.stateInAir=="right"):
                    self.speed[0] = 1
                    
        if(self.state=="speedtop"):
            if(count==1):
                self.speed[1] = 0
                self.state = "jumpdown"
                if(self.stateInAir=="left"):
                    self.speed[0] = -1
                if(self.stateInAir=="right"):
                    self.speed[0] = 1
                    
        if(self.state=="jumpdown"):
            if(count==10):
                self.speed[1] = 1
                self.state = "ground"
                if(self.stateInAir=="left"):
                    self.speed[0] = -1
                if(self.stateInAir=="right"):
                    self.speed[0] = 1
               
        if(self.state=="ground"):
            if(count==11):
                self.speed[1] = 0
                if(self.stateInAir=="left"):
                    self.speed[0] = -1
                    self.stateInAir = "notInAir" 
                if(self.stateInAir=="right"):
                    self.speed[0] = 1
                    self.stateInAir = "notInAir" 
        self.move()     
        return count+1
        
        
        
