# Bruce A. Maxwell
# January 2015
#
# Pygame Tutorial Example 1
#
# Creates a static scene and then waits for an event to quit
#

####################### Setup #########################
# useful imports
import sys

# import pygame
import pygame

# initialize pygame
pygame.init()

# initialize the fonts
try:
	pygame.font.init()
except:
	print "Fonts unavailable"
	sys.exit()

# create a screen (width, height)
screen = pygame.display.set_mode( (640, 480) )

####################### Making Content #########################

# load some images
startBackground = pygame.image.load( "heartPicture.jpeg" ).convert_alpha()

# create a font
afont = pygame.font.SysFont( "Cambria", 72, bold=True )

# render a surface with some text
text = afont.render( "RUSTY HEART", True, (0, 0, 0) )

####################### Filling the Screen #########################

# clear the screen with white
screen.fill( (255, 255, 255) )

# now draw the surfaces to the screen using the blit function
screen.blit( startBackground, (-30, -30) )

# create a font
afont = pygame.font.SysFont( "Times New Roman", 60, bold=True )

# render a surface with some text
start = afont.render( "START", True, (255, 255, 255) )

# draw a rectangle behind the text
pygame.draw.rect( screen, (70, 210, 80), pygame.Rect( (220, 180), (210, 80) ) )

# blit the text surface onto the screen
screen.blit( text, (100, 100) )
screen.blit( start, (230, 190) )
# update the screen
pygame.display.update()

####################### Main Event Loop #########################
# go into a holding pattern until someone clicks a mouse or hits a key
print "Entering main loop"
while 1:
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN :
			sys.exit()

		if event.type == pygame.KEYDOWN:
			sys.exit()

		if event.type == pygame.QUIT:
			sys.exit()

		
# done
print "Terminating"
