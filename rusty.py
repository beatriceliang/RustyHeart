'''
Itrat Akhter, Catherine Alden, Luis Henriquez-Perez, Beatrice Liang, Tiffany Lam, Shama Ramos
Rusty
CS369 
January 2015
'''
import sys
import random
import pygame
class Rusty:
    def __init__(self,start):
        ''' initializes rusty class which holds its images and location'''
        pygame.init()
        self.start = start
        self.speed = [0,0]
        #images
        self.rightImage = pygame.image.load("images/rusty/rightrusty.png").convert_alpha()
        self.leftImage = pygame.image.load("images/rusty/leftrusty.png").convert_alpha()
        self.waveImage = pygame.image.load("images/rusty/rustysmaller.png").convert_alpha()
        self.image = self.rightImage

        self.left = False #direction rusty is facing
        self.rect = self.image.get_rect().move(self.start[0],self.start[1])
        self.justJumped = False
        self.box = None
        self.doneWave = "notWaving"
        self.fast = False
        self.lives = 3
        self.collectedHearts = []
        self.heart = pygame.mixer.Sound( "music/sounds/heart.wav" )
    def reset(self):
        '''places rusty back to the beginning of the screen'''
        self.rect = self.image.get_rect().move(self.start[0],self.start[1])
    def speedLeft(self):
        '''moves rusty left'''
        if(self.doneWave=="doneWaving"):
            self.rect = self.leftImage.get_rect().move(self.rect.left,self.rect.top)
            self.doneWave = "notWaving"
        if(self.doneWave=="waving"):
            self.doneWave="doneWaving"
        self.image = self.leftImage
        self.left = True
        if self.fast:
            self.speed[0]=-8
        else:
            self.speed[0]=-5
    def speedRight(self):
        '''moves rusty right'''
        if(self.doneWave=="doneWaving"):
                self.rect = self.rightImage.get_rect().move(self.rect.left,self.rect.top)
                self.doneWave = "notWaving"
        if(self.doneWave=="waving"):
                self.doneWave="doneWaving"
        self.image = self.rightImage
        self.left = False
        if self.fast:
            self.speed[0]=8
        else:
            self.speed[0]=5
    def stop(self):
        '''makes rusty stop'''
        self.speed[0] = 0
        
    def wave(self):
        '''pointless, makes rusty wave'''
        self.image = self.waveImage
        self.rect = self.waveImage.get_rect().move(self.rect.left,self.rect.top)
        self.doneWave = "waving"
        
    def jump(self):
        '''makes rusty jump'''
        if not self.justJumped:
            self.speed[1]= -75
            self.justJumped = True
    def isOnBox(self,box):
        '''checks if rusty is on a box or not'''
        return (box.rect.centery +box.rect.height/2 >= self.rect.centery +self.rect.height/2) and (box.rect.centery-box.rect.height/2 <= self.rect.centery + self.rect.height/2) and (box.rect.centerx + box.rect.width/2 >= self.rect.centerx) and (box.rect.centerx-box.rect.width/2 <= self.rect.centerx)
    def move(self,boxes,diffX):
        ''' checks the conditions of rusty to handles its movements'''
        notOn = True
        b = None
        i = 0
        
        for box in boxes:
            if box.type=="heart" and box.visible==True:
                continue
            if box.type != "door" or (box.type=="heart" and box.visible==True):
                
                if self.rect.colliderect(box.rect):
                    box.collide = True
                    if box.type=="heart" and not box.rect.colliderect(boxes[i+1].rect):
                            box.visible=True
                            self.heart.play()
                            self.collectedHearts.append(box.location)
                            self.lives +=1
                            
                            
                else:
                    box.collide = False
                if box.rect.left <640 and box.rect.right>0:
                    if not self.justJumped and self.left and self.rect.colliderect(box.rect) and self.rect.left <= box.rect.right and self.rect.right >=box.rect.right and self.rect.bottom > box.rect.centery:
                        if not(box.type=="heart" and box.visible==True):
                            self.stop()
                        
                    elif not self.justJumped and not self.left and self.rect.colliderect(box.rect) and self.rect.right >= box.rect.left and self.rect.left <= box.rect.left and self.rect.bottom > box.rect.centery:
                        if not(box.type=="heart" and box.visible==True):
                            self.stop()
                       
                    if box.type =="metal" and self.rect.centerx > box.rect.left and self.rect.centerx <box.rect.right and self.rect.top >= box.rect.bottom and self.rect.top < box.rect.bottom + box.rect.height:
                        self.justJumped = False
                        self.speed[1] = 0
                    
                    if self.isOnBox(box):
                        if box == self.box or box.type=="heart":
                            continue
                        notOn = False
                        b = box
            i+=1 

        if notOn ^ self.justJumped:
            self.speed[1] +=  2
        else:
            self.speed[1] = 0
            self.justJumped = False
        if b != None and not self.justJumped:
            self.speed[1] = b.rect.top-self.rect.height-self.rect.top
        self.rect.move_ip(self.speed[0]-diffX, self.speed[1])
if __name__ == '__main__':
    print "please go to RustyHeart.py to play"
 
        
