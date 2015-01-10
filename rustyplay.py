#Testing rusty

####################### Setup #########################
# useful imports
import sys
import random
import rusty
# import pygame
import pygame

# initialize pygame
pygame.init()
rus = rusty.Rusty([0,0],[0,0],0)

# initialize the fonts
try:
	pygame.font.init()
except:
	print "Fonts unavailable"
	sys.exit()

# create a game clock
gameClock = pygame.time.Clock()


# create a screen (width, height)
screen = pygame.display.set_mode( (640, 480) )

####################### Making Content #########################

# load some images


rusdude = pygame.image.load( "Broom.png" ).convert_alpha()

# create a font
afont = pygame.font.SysFont( "Helvetica", 20, bold=True )

# render a surface with some text
text = afont.render( "Clean up time", True, (0, 0, 0) )

# load some sound
sweep = pygame.mixer.Sound( "sweep.wav" )


####################### Filling the Screen #########################

# A function that draws all of the static background elements
def drawBkg(screen, text, refresh, rect=None):
	# clear the screen with white
	if rect == None:
		screen.fill( (255, 255, 255) )

		# blit the text surface onto the screen
		screen.blit( text, (10, 10) )

		refresh.append( screen.get_rect() )
	else:
		screen.fill( (255, 255, 255), rect )

		# blit the text surface onto the screen if it is inside the rectangle
		screen.fill( (255, 255, 255), text.get_rect().move(10, 10).clip( rect ) )

		trect = text.get_rect().move(10, 10) # rectangle in which to
											 # draw the text
											 
		clippedRect = trect.clip( rect ) # intersection of the text
										 # screen rectangle and the
										 # area to update

		# blit the text into the area to update, the second rectangle
		# indicates which part of the text to use
		urect = screen.blit( text, clippedRect, clippedRect.move(-10,-10) )

		# refresh the rectangle
		refresh.append( rect )


############## Setting up the Broom as a sprite ################

# get the current mouse information, and make the cursor invisible if
# it is focused on the game window
pygame.event.pump()
# if pygame.mouse.get_focused():
#	  pygame.mouse.set_visible(False)


# get the mouse position and put the broom so it is centered on the
# mouse location
tpos = pygame.mouse.get_pos()
trect = rusdude.get_rect()
rusdudeRect = rusdude.get_rect().move( tpos[0] - trect.width/2, tpos[1] - trect.height/2 )
rusDudeActiveRect = pygame.Rect((4, 41),(106, 82))

# blit the broom to the screen and update the display
screen.blit( rusdude, rusdudeRect )


####################### Main Event Loop #########################
# set up the refresh rectangle container
refresh = []
drawBkg( screen, text, refresh )

# update the display before we start the main loop
pygame.display.update()


# respond to mouse motion events until someone clicks a mouse or hits a key
print "Entering main loop"
while 1:
      
    # handle events and erase things
    for event in pygame.event.get():
    	
        if event.type == pygame.MOUSEMOTION:
            # erase the existing broom
            drawBkg( screen, text, refresh, rusdudeRect )
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            sys.exit()
        
        if event.type == pygame.KEYDOWN:   
            if event.key == pygame.K_LEFT:
            	rus.speedLeft()
                if(rus.alreadyPressed[0]!=0):
                    rus.alreadyPressed[1] = 1
            if event.key == pygame.K_RIGHT:
                rus.speedRight()
                if(rus.alreadyPressed[0]!=0):
                    rus.alreadyPressed[2] = 1
            if event.key == pygame.K_UP:
            	rus.speedUp()
            	rus.alreadyPressed[0] = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
            	if(rus.alreadyPressed[1]!=2):
            	    rus.speedRight()
                rus.alreadyPressed[1] = 0
            if event.key == pygame.K_RIGHT:
                if(rus.alreadyPressed[2]!=2):
            	    rus.speedLeft()
            if event.key == pygame.K_UP:
                rus.changeState(1)
                rus.alreadyPressed[0] = 0
        if event.type == pygame.QUIT:
            sys.exit()
    drawBkg(screen,text,refresh,rusdudeRect)
   # print "alreadyPressed"
    #print rus.alreadyPressed
    
    if(rus.state==2):
    	rus.comeToGround()
    if (rus.state==1):
    	rus.speedDown()
	rus.changeState(2)
	continue
    
    rus.move()
    
    if(rus.alreadyPressed[0]==1):
    	rus.changeState(2)
    	rus.alreadyPressed[0] = 2
    	continue
    if(rus.alreadyPressed[1]==1):
        rus.speedRight()
        rus.alreadyPressed[1] = 2
        continue
    if(rus.alreadyPressed[2]==1):
        rus.speedLeft()
        rus.alreadyPressed[2] = 2
        continue
    # If the game is in focus, draw things
    rusdudeRect = pygame.Rect((rusdudeRect.width/2+rus.location[0],rusdudeRect.height/2+rus.location[1]),(rusdudeRect.width,rusdudeRect.height))
    screen.blit(rusdude,rusdudeRect)
    refresh.append(rusdudeRect)

    # update the parts of the screen that need it
    pygame.display.update( refresh )

    # clear out the refresh rects
    refresh = []

    # throttle the game speed to 30fps
    gameClock.tick(30)
		
# done
print "Terminating"
