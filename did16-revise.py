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
# V13 added drop shadow, for now it is fixed at 3 but could be passed to font_process
# V15 adding pay input
# V16 cleaned up polling for free vs pay input
# V16 now under GIT control

# IMPORTS START --------------------------------------------------
# makes extensive use of pygame to blit the screen
from random import randrange, shuffle, random
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
Free = False # playing for free flag
Win = False # winner flag
PayOut = 50


 # percentage of losers
image_centerx = 960
image_centery = 540


# VARIABLE INITIALIZE END _________________________________________

# GPIO PORTS START ------------------------------------------------
    # Define Ports if PortList starts with a 0 it is output
    # if it starts with a 1 it is input
# Port assignments 1 [in,4-B1,17-B2,27-B3,22-B4,5-B5,6-Rst]
PortList = [1,4,17,27,22,5,6]
# Port assignments 2 [in,13-Free,26-Pay]
PortList2 = [1,13,26]
# Port assignments 3 [out, 23-Bell, 16 Lights]
PortList3 = [0, 23, 16]



# GPIO PORT END ___________________________________________________

# DEFINE CLASES START ---------------------------------------------

# DEFINE CLASES END _______________________________________________

# ///////////////////////////////////////////////////////////////////
# METHODS AND FUNCTIONS START --------------------------------------
def init():
    # initialize code can go here
    pass

def portassign(ports):
    # assign ports based on index[0] if 0 Output else Input
    
    if ports[0] == 0:
        print('Output')
        for index in range(1, len(ports)):
            GPIO.setup(ports[index], GPIO.OUT)
            
            print(ports[index])
    else:
        print('Input')
        for index in range(1, len(ports)):
            GPIO.setup(ports[index], GPIO.IN, pull_up_down = GPIO.PUD_UP)
            print(ports[index])
            




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
    global Free
    global Win
    white = (255, 255, 255)
    black = (0, 0, 0,)
    red = (255, 50, 50)
    display.blit(bg_dol, (0, 0))
    greeting = 'Press Start for free play'
    font_process(60, greeting, white, 100, 200)
    greeting = 'or'
    font_process(60, greeting, white, 100, 280)
    greeting = 'Make a Donation and get a chance to win a Bonehenge Prize'
    font_process(60, greeting, white, 100, 360)
    greeting = '(Prizes are awarded randomly and are not dependent on final quiz score)'
    font_process(30, greeting, white, 100, 1000)
    pygame.display.flip()
    
    # Select if this is a paid or free play
    while GPIO.input(PortList2[1]) == GPIO.HIGH and GPIO.input(PortList2[2]) == GPIO.HIGH:
        sleep(.05)
        #print('in pay detection')
        if GPIO.input(PortList2[1]) == GPIO.LOW:
            sleep(.08)
            Free = True
            Win = False
            print('Free Play')
                
        if GPIO.input(PortList2[2]) == GPIO.LOW:
            print('PLAYBACK SHOULD HAPPEN')
            sleep(.08)
            Free = False
            Win = False # set it false for now
            Rnd_Chance = int(random() * 100 )
            play_sound('Yay.mp3', .5)
            
            if Rnd_Chance >= PayOut:
                Win = True
                print('A Winner')
                
            else:
                Win = False
                print('A Loser')
            
 
    display.blit(bg_dol, (0, 0))
    greeting = 'Hello Welcome to ID the Dolphin'
    font_process(60, greeting, white, 100, 100)
    pygame.display.flip()
    sleep(2)

    info = 'We can identify individuals by their dorsal fin shape'
    font_process(50, info, white, 100, 200)
    pygame.display.flip()
    # sleep(.5)

    inst = 'See if you can match one on the bottom row to the top picture'
    font_process(50, inst, white, 30, 300)
    pygame.display.flip()
    sleep(5)
    display.blit(bg_dol, (0, 0))
    pygame.display.flip()


def font_process(size, message, color, x, y):
    # attempt to combine all font operations into one call that
    # renders and blits the text
    
    black = (0,0,0)
    d_shadow = 3
    font = pygame.font.SysFont('FreeSans', size, True, False)
    render_message = font.render(message, True, color)
    if d_shadow:
        render_ds = font.render(message, True, black)
        render_ds_rect = render_message.get_rect()
    # attempt to center works
    render_msg_rect = render_message.get_rect()
    render_cent = render_msg_rect[1]

    render_msg_rect.center = (image_centerx, y) # (x,y) x = screen center

    if d_shadow:
        render_ds_rect.center = (image_centerx + d_shadow, y + d_shadow)
        display.blit(render_ds, render_ds_rect)
    display.blit(render_message, render_msg_rect)

def play_sound(sfile,vol):
    pygame.mixer.music.set_volume(vol)
    pygame.mixer.music.load(gpath + sfile)
    pygame.mixer.music.play()

def play_loop():
    pos_resp =['Correct','Got it, Nice','Right','Good Pick','Way to go','On a roll']
    neg_resp =['Sorry','Nope','Not that one','Too bad','Gotcha','Maybe next time']
    final_resp =['Better Try Again','Keep Working at it','Not Bad','Pretty Good','Excellent Nice Job','100% Wow!']
    right_ans = 0  # scoring
    wrong_ans = 0  # scoring
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    turn = 0  # used to access comp_pic
    display_pics = [x for x in range(max_pic)]  # this is a random list of the computer pics
    shuffle(display_pics)  # scramble them these are the index numbers 
    # use display_pic to put up that pic on top (chalange pic)
    # use rnums to show all pics on bottom (computer pics)
    GPIO.output(PortList3[2], True) # turn on the button lights
    for items in rnums:
        shuffle_pics()
        display_pic = display_pics[turn]  # picks a new one each turn
        send_to_screen(display_pic, rnums, 'Testing')  # put up the challenge screen

        #  go get user response
        resp = which_pic2() #  go and wait for button input return pic#
        print('back from which pic resp= '+ str(resp) + ' for pic# ' + str(display_pic))

        if resp == -1:
            score_msg = ('Delay Timeout')
            break

        if rnums[resp] == display_pic:
            pgm_rsp = pos_resp[randrange(len(pos_resp))]
            right_ans = right_ans + 1
            play_sound('Quick-win.mp3', .3)
            print(pgm_rsp)
        else:
            pgm_rsp = neg_resp[randrange(len(neg_resp))]
            print(pgm_rsp)
            wrong_ans = wrong_ans + 1
            play_sound('Downer.mp3', .2)
        score_msg = ('Current Score  '+ str(right_ans)+ ' right  '+ str(wrong_ans)+' wrong')

        # clear screen of old score and put up new one
        display.blit(bg_dol, (0, 0))
        font_process(60, score_msg, white, 500, 500)
        font_process(60, pgm_rsp, white, 500, 550)
        turn = turn + 1

    # final score
    score_msg = ('Final Score  '+ str(right_ans)+ ' right  '+ str(wrong_ans)+' wrong')
    final_msg = (final_resp[right_ans])
    display.blit(bg_dol, (0, 0))
    font_process(60, score_msg, white, 100, 400)
    font_process(60, final_msg, white, 100, 500)
    if Win == True:
        font_process(75,'You are a WINNER!!',red, 100, 600)
        font_process(75,'Please see one of our Staff for your prize',red, 100, 700)
        play_sound('fanfare.mp3', 1)
    
    if Win == False and Free == False:
        font_process(60,'Sorry, you are not a winner this time', blue, 100, 600)

    pygame.display.flip()
    GPIO.output(PortList3[2], False) # turn off the button lights

    #  add delay here
    sleep(5)

def which_pic2():
    # this version uses the push buttons instead of touch screen
    # decided to do it as a polling loop rather than interrupts
    start_time = time()
    end_time = time()
    ans = -1 # this value will be set and returned to Play_Loop
    while end_time - start_time < 10: # delay in seconds till loop ends
        end_time = time()
        # run through all assigned pins
        # we start with an index of 1 to skip the Input/Output selector
        for index in range(1, len(PortList)):
            sleep(.03) # debounce time
            if GPIO.input(PortList[index]) == GPIO.LOW:
                ans = PortList[index] # first pull the value
                ans = PortList.index(PortList[index]) -1 # then locate it in the list
                print('Button Press: ',str(ans))
                # special case to reset DOESN'T WORK
                if ans == 5:
                    ans = -1
        if ans in range(0, 5):
            break #  get out of loop
            

    return ans



def which_pic():
    while True:
        #  find out where the mouse/touch happened and return value
        #  this is an endless loop until right input
        #  legacy code from touch screen, no longer used
        event = pygame.event.wait()
        ans = -1
        click_spot = (0, 0)
        #  setting a timer here so if they walk away it will cycle through
        #  and reset
        time_out = pygame.USEREVENT
        pygame.time.set_timer(time_out, 40000) #  40 seconds
        # if idle for too long bail out
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


def send_to_screen(display_me, rnums, caption):

    # display_pic is challenge picture
    # should do the background graphic here
    your_pic = [uw1, uw2, uw3, uw4, uw5]
    comp_pic = [cw1, cw2, cw3, cw4, cw5]

    # display the challenge pic
    display.blit(comp_pic[display_me],(840,10)) # Challange pic location
    # display the other pictures from list on bottom
    choicesx = 50
    choicesy = 700
    i = 0
    #print('send to screen has rnums as ', str(rnums))
    for items in rnums:
        # use the rnums list to index your_pic list to get the pictures
        display.blit(your_pic[rnums[i]],(choicesx, choicesy))
        i = i + 1
        choicesx = choicesx + 380 # spacing for choices pics


    pygame.display.flip()



# METHODS AND FUNCTIONS END _________________________________________
# ///////////////////////////////////////////////////////////////////


# INITIALIZE RUN ONCE CODE START ------------------------------------
pygame.init()
pygame.mixer.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'
clock = pygame.time.Clock()
screen_width = 1920
screen_height = 1080
bgColor = (0,0,0)
size = (screen_width, screen_height)

# assign I/O ports
portassign(PortList) # main buttons
portassign(PortList2) # free or pay
portassign(PortList3) # output for bell and lights relays
GPIO.output(PortList3[1], False) # no bell
GPIO.output(PortList3[2], False) # no lights

# for developement uncomment the line below
#display = pygame.display.set_mode(size)
# for autostart to work properly uncomment the line below
#display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
display = pygame.display.set_mode((1920,1080))

pygame.display.set_caption('ID The Dolphin')
pygame.mixer.music.set_volume(1.0)
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
# path to sounds
awefile = gpath + 'Awe.mp3'
yayfile = gpath + 'Yay.mp3'
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
# load sounds


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
            play_loop() # this is where all the work is done might want to break it up





    except KeyboardInterrupt:
        #cleanup at end of program
        print('   Shutdown')
        GPIO.cleanup()

if __name__ == '__main__':
    main()