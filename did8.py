#!/usr/bin/python3

# V DID6 changed name and moved pygame stuff
# V6 got display working now going to rearrange
# V7 long form font renders going to try to streamline
# IMPORTS START --------------------------------------------------
# makes extensive use of pygame to blit the screen
from random import randrange, shuffle
from time import sleep
import sys, pygame
from pygame.locals import *
import pygame.font
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import os


# IMPORTS END ____________________________________________________

# VARIABLE INITIALIZE START----------------------------------------
max_pic = 5
rnums = []
display_pic = 0
resp = 0



# VARIABLE INITIALIZE END _________________________________________

# GPIO PORTS START ------------------------------------------------

# GPIO PORT END ___________________________________________________

# DEFINE CLASES START ---------------------------------------------

# DEFINE CLASES END _______________________________________________

# ///////////////////////////////////////////////////////////////////
# METHODS AND FUNCTIONS START --------------------------------------
def init():
    # initialize code can go here
    pass


def shuffle_pics():
    # uses max_pic to randomize pictures
    global display_pic
    global rnums

    #display_pic = randrange(max_pic)
    print('selected picture ' + str(randrange(max_pic)))
    rnums = [x for x in range(max_pic)]
    shuffle(rnums)
    # rnums is a shuffled list of the picture numbers for choosing
    print('rnums is now ' + str(rnums))
    # iterate to build a list of random numbers

def show_rules():
    # display rules and wait for input
    # define font colors
    white = (255, 255, 255)
    black = (0, 0, 0,)
    red = (255, 50, 50)
    display.blit(bg_dol, (0, 0))

    greeting = 'Hello Welcome to ID the Dolphin'
    font_process(40, greeting, black, 100, 100)
    pygame.display.flip()
    sleep(2)

    info = 'We can identify individuals by their dorsal fin shape'
    font_process(25, info, black, 150, 200)
    pygame.display.flip()
    sleep(2)

    inst = 'See if you can match one on the top row to the bottom picture'
    font_process(25, inst, red, 30, 400)
    pygame.display.flip()
    sleep(2)


def font_process(size, message, color, x, y):
    # attempt to combine all font operations into one call that
    # and blits the text
    font = pygame.font.SysFont('FreeSans', size, True, False)
    render_message = font.render(message, True, color)
    display.blit(render_message, (x, y))

def play_loop():
    pos_resp=['Correct','Got it, Nice','Right','Good Pick','Way to go','On a roll']
    neg_resp=['Sorry','Nope','Not that one','Too bad','Gotcha','Maybe next time']
    final_resp=['Better Try Again','Keep Working at it','Not Bad','Pretty Good','Excellent Nice JOb','100% Wow!']
    right_ans = 0 # scoring
    wrong_ans = 0 # scoring
    turn = 0 # used to access comp_pic
    display_pics = [x for x in range(max_pic)] # this is a random list of the left pic
    shuffle(display_pics) # scramble them these are the index numbers for
    # use display_pic to put up that pic on left
    # use rnums to show all pics on right
    for items in rnums:
        shuffle_pics()
        display_pic = display_pics[turn] # picks a new one each turn
        # need to blit the screen with all the pics here possible caption Round 1 etc
        send_to_screen(display_pic, rnums, 'Testing') # put up the challenge screen

        resp = int(input('Make Selection -- Display Pic = '+ str(display_pic)+'  Choices '+ str(rnums)))
        # wait for selection
        if rnums[resp] == display_pic:
            pgm_rsp = pos_resp[randrange(len(pos_resp))]
            right_ans = right_ans + 1
            print(pgm_rsp)
        else:
            pgm_rsp = neg_resp[randrange(len(neg_resp))]
            print(pgm_rsp)
            wrong_ans = wrong_ans + 1
        print('Current Score, '+ str(right_ans)+ ' right.  '+ str(wrong_ans)+' wrong')
        turn = turn + 1
    # final score
    print(final_resp[right_ans])
    # add delay here
    sleep(5)

def send_to_screen(left_pic, rnums, caption):

    # left_pic is the still on the left (bottom), right_pics (top) is a list, caption a string
    # should do the background graphic here
    your_pic = [uw1, uw2, uw3, uw4, uw5]
    comp_pic = [cw1, cw2, cw3, cw4, cw5]


    display.blit(comp_pic[left_pic],(350,240))
    # display the other pictures from list on top (was right)
    rightx = 20
    righty = 10
    i = 0
    #print('send to screen has rnums as ', str(rnums))
    for items in rnums:

        # use the rnums list to index your_pic list to get the pictures
        display.blit(your_pic[rnums[i]],(rightx, righty))

        i = i + 1
        rightx = rightx + 166


    pygame.display.flip()


def score():
    # for one less than the max
    # display score x of y and random encouragement

    global display_pic
    global rnums
    global resp
    # when max is reached display final score
    pass

# METHODS AND FUNCTIONS END _________________________________________
# ///////////////////////////////////////////////////////////////////


# INITIALIZE RUN ONCE CODE START ------------------------------------
pygame.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'
clock = pygame.time.Clock()
screen_width = 800
screen_height = 480
bgColor = (0,0,0)
size = (screen_width, screen_height)
display = pygame.display.set_mode(size)

pygame.display.set_caption('ID The Dolphin')
# load the pics 'c' for computer 'u' for user
uwhale1 = '/home/pi/MyCode/whale1.jpg'
uwhale2 = '/home/pi/MyCode/whale2.jpg'
uwhale3 = '/home/pi/MyCode/whale3.jpg'
uwhale4 = '/home/pi/MyCode/whale4.jpg'
uwhale5 = '/home/pi/MyCode/whale5.jpg'
cwhale1 = '/home/pi/MyCode/1whale1.jpg'
cwhale2 = '/home/pi/MyCode/2whale2.jpg'
cwhale3 = '/home/pi/MyCode/3whale3.jpg'
cwhale4 = '/home/pi/MyCode/4whale4.jpg'
cwhale5 = '/home/pi/MyCode/5whale5.jpg'
bg_dolphins = '/home/pi/MyCode/dolphins.jpg'
# now to actually load them same letters this has to be done in two steps
uw1 = pygame.image.load(uwhale1).convert_alpha()
uw2 = pygame.image.load(uwhale2).convert_alpha()
uw3 = pygame.image.load(uwhale3).convert_alpha()
uw4 = pygame.image.load(uwhale4).convert_alpha()
uw5 = pygame.image.load(uwhale5).convert_alpha()
cw1 = pygame.image.load(cwhale1).convert_alpha()
cw2 = pygame.image.load(cwhale2).convert_alpha()
cw3 = pygame.image.load(cwhale3).convert_alpha()
cw4 = pygame.image.load(cwhale4).convert_alpha()
cw5 = pygame.image.load(cwhale5).convert_alpha()
bg_dol = pygame.image.load(bg_dolphins).convert_alpha()
# these lists point to the picture files, there are 5 matching pairs
# currently they are the same pictures but will be replaced


# INITIALIZE RUN ONCE CODE END _________________________________________

# ************************ MAIN START **********************************

def main():
    try:
        init()
        # note init only runs once
        while 1:
            print('Main Program')
            show_rules()
            shuffle_pics()
            play_loop()




    except KeyboardInterrupt:
        #cleanup at end of program
        print('   Shutdown')
        GPIO.cleanup()

if __name__ == '__main__':
    main()