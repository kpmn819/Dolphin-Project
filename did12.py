#!/usr/bin/python3

# V DID6 changed name and moved pygame stuff
# V6 got display working now going to rearrange
# V7 long form font renders going to try to streamline
# V8 got the screens working
# V9 attempt to detect mouse clicks
# V9 mouse clicks good tried to center text, no good
# V10 working version, need to add escape timeout
# V11 larger pictures in graphics folder
# V12 got time_out delay working had to extend to 40 seconds so as not to time out early

# IMPORTS START --------------------------------------------------
# makes extensive use of pygame to blit the screen
from random import randrange, shuffle
from time import sleep, time
import sys, pygame
from pygame.locals import *
import pygame.font
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import os
FPS = 30


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

    # display_pic = randrange(max_pic)
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
    greeting = 'Tap screen to play'
    font_process(40, greeting, white, 100, 100)
    pygame.display.flip()
    # pause screen here
    while True:
        event = pygame.event.wait()
        click_spot = (801, 481)
        # if any mouse button is pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_spot =(pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])

        if 0 <= click_spot[0] <= 800 and 0 <= click_spot[1] <= 480:
            break  #  click anywhere to continue


    display.blit(bg_dol, (0, 0))
    greeting = 'Hello Welcome to ID the Dolphin'
    font_process(40, greeting, white, 100, 100)
    pygame.display.flip()
    sleep(2)

    info = 'We can identify individuals by their dorsal fin shape'
    font_process(25, info, white, 100, 150)
    pygame.display.flip()
    sleep(4)

    inst = 'See if you can match one on the top row to the bottom picture'
    font_process(25, inst, white, 30, 175)
    pygame.display.flip()
    sleep(6)
    display.blit(bg_dol, (0, 0))
    pygame.display.flip()

def font_process(size, message, color, x, y):
    # attempt to combine all font operations into one call that
    # renders and blits the text

    font = pygame.font.SysFont('FreeSans', size, True, False)
    render_message = font.render(message, True, color)
    # attempt to center works
    render_msg_rect = render_message.get_rect()
    render_cent = render_msg_rect[1]
    #print('render center =' + str(render_cent))
    render_msg_rect.center = (400, y)
    display.blit(render_message, render_msg_rect)

def play_loop():
    pos_resp =['Correct','Got it, Nice','Right','Good Pick','Way to go','On a roll']
    neg_resp =['Sorry','Nope','Not that one','Too bad','Gotcha','Maybe next time']
    final_resp =['Better Try Again','Keep Working at it','Not Bad','Pretty Good','Excellent Nice Job','100% Wow!']
    right_ans = 0  # scoring
    wrong_ans = 0  # scoring
    white = (255, 255, 255)
    turn = 0  # used to access comp_pic
    display_pics = [x for x in range(max_pic)]  # this is a random list of the left pic
    shuffle(display_pics)  # scramble them these are the index numbers for
    # use display_pic to put up that pic on left
    # use rnums to show all pics on right
    for items in rnums:
        shuffle_pics()
        display_pic = display_pics[turn]  # picks a new one each turn
        # need to blit the screen with all the pics here possible caption Round 1 etc
        send_to_screen(display_pic, rnums, 'Testing')  # put up the challenge screen

        #  go get user response
        resp = which_pic() #  go and wait for proper mouse input return pic#
        print('back from which pic resp= '+ str(resp))

        #if resp == -1:
        #    score_msg = ('Delay Timeout')
        #    break

        if rnums[resp] == display_pic:
            pgm_rsp = pos_resp[randrange(len(pos_resp))]
            right_ans = right_ans + 1
            #print(pgm_rsp)
        else:
            pgm_rsp = neg_resp[randrange(len(neg_resp))]
            #print(pgm_rsp)
            wrong_ans = wrong_ans + 1
        score_msg = ('Current Score  '+ str(right_ans)+ ' right  '+ str(wrong_ans)+' wrong')

        # clear screen of old score
        display.blit(bg_dol, (0, 0))
        font_process(40, score_msg, white, 100, 200)
        font_process(40, pgm_rsp, white, 100, 250)
        turn = turn + 1
    # final score
    final_msg = (final_resp[right_ans])
    display.blit(bg_dol, (0, 0))
    font_process(40, score_msg, white, 100, 200)
    font_process(60, final_msg, white, 100, 300)
    pygame.display.flip()

    #  add delay here
    sleep(5)

def which_pic():
    while True:
        #  find out where the mouse/touch happened and return value
        #  this is an endless loop until right input
        event = pygame.event.wait()
        ans = -1
        click_spot = (0, 0)
        #  setting a timer here so if they walk away it will cycle through
        #  and reset
        time_out = pygame.USEREVENT
        pygame.time.set_timer(time_out, 40000) #  40 seconds
        # if idle for too long bail out
        #  PROBLEM SCORE AFTER TIME OUT IS NOT RESET STARTS WITH FIRST TURN
        if event.type == time_out:
            print('time out happened')
            ans = 0
            break
        #  press or touch mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_spot =(pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
            pygame.event.clear() #  flush out any time_out events


        if 5  <= click_spot[0] <= 155 and 40 <= click_spot[1] <= 190:
            print('selected 0')
            ans = 0
        if 165 <= click_spot[0] <= 315 and 40 <= click_spot[1] <= 190:
            ans = 1
            print('selected 1')
        if 325 <= click_spot[0] <= 475 and 40 <= click_spot[1] <= 190:
            ans = 2
            print('selected 2')
        if 485 <= click_spot[0] <= 635 and 40 <= click_spot[1] <= 190:
            ans = 3
            print('selected 3')
        if 645 <= click_spot[0] <= 795 and 40 <= click_spot[1] <= 190:
            ans = 4
            print('selected 4')
        if 0 <= click_spot[0] <= 50 and 430 <= click_spot[1] <= 480:
            # extreem lower left hidden exit
            pygame.quit()
            sys.exit()
        if ans in range(0, 5):
            break #  get out of endless loop
    return ans


def send_to_screen(left_pic, rnums, caption):

    # left_pic is the still on the left (bottom), right_pics (top) is a list, caption a string
    # should do the background graphic here
    your_pic = [uw1, uw2, uw3, uw4, uw5]
    comp_pic = [cw1, cw2, cw3, cw4, cw5]

    # display the challenge pic
    display.blit(comp_pic[left_pic],(325,300))
    # display the other pictures from list on top (was right)
    rightx = 5
    righty = 20
    i = 0
    #print('send to screen has rnums as ', str(rnums))
    for items in rnums:

        # use the rnums list to index your_pic list to get the pictures
        display.blit(your_pic[rnums[i]],(rightx, righty))
        i = i + 1
        rightx = rightx + 160


    pygame.display.flip()



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
#display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

pygame.display.set_caption('ID The Dolphin')
# load the pics 'c' for computer 'u' for user
gpath = '/home/pi/MyCode/graphics/'
udol1 = gpath + '1dol.jpg'
udol2 = gpath + '2dol.jpg'
udol3 = gpath + '3dol.jpg'
udol4 = gpath + '4dol.jpg'
udol5 = gpath + '5dol.jpg'
cdol1 = gpath + '1dol1.jpg'
cdol2 = gpath + '2dol2.jpg'
cdol3 = gpath + '3dol3.jpg'
cdol4 = gpath + '4dol4.jpg'
cdol5 = gpath + '5dol5.jpg'
bg_dolphins = gpath + 'dolphins3.jpg'
# now to actually load them same letters this has to be done in two steps
uw1 = pygame.image.load(udol1).convert_alpha()
uw2 = pygame.image.load(udol2).convert_alpha()
uw3 = pygame.image.load(udol3).convert_alpha()
uw4 = pygame.image.load(udol4).convert_alpha()
uw5 = pygame.image.load(udol5).convert_alpha()
cw1 = pygame.image.load(cdol1).convert_alpha()
cw2 = pygame.image.load(cdol2).convert_alpha()
cw3 = pygame.image.load(cdol3).convert_alpha()
cw4 = pygame.image.load(cdol4).convert_alpha()
cw5 = pygame.image.load(cdol5).convert_alpha()
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