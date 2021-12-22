#!/usr/bin/python3


# V16 now under GIT control
# try a push when logged in

# IMPORTS START --------------------------------------------------
# makes extensive use of pygame to blit the screen
#from random import randrange, shuffle, random, sample
import random
from random import randrange, shuffle
from time import sleep, time
import sys, pygame
from pygame.locals import *
import pygame.font
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import os
import csv
FPS = 30
game1 = False
# game 2 variables
list_file = 'qna_pool.csv'
file_error = False
row_count = 0
donation = False


# IMPORTS END ____________________________________________________

# VARIABLE INITIALIZE START----------------------------------------
max_pic = 5
rnums = []
display_pic = 0
resp = 0
free = False # playing for free flag
win = False # winner flag
payout = 33 # percentage of winners

image_centerx = 960
image_centery = 540
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# may be used later to select game 1 or 2
game1 = True


# VARIABLE INITIALIZE END _________________________________________

# GPIO PORTS START ------------------------------------------------
# Define Ports if portList starts with a 0 it is output
# if it starts with a 1 it is input
# Port assignments 1 [in,4-B1,17-B2,27-B3,22-B4,5-B5,6-Rst]
portList = [1,4,17,27,22,5,6]
# Port assignments 2 [in,13-Free,26-Pay]
portList2 = [1,13,26]
# Port assignments 3 [out, 23-Bell, 16 Lights]
portList3 = [0, 23, 16]
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

def show_rules(picture):
    # display rules and wait for input
    # define font colors
    global free
    global win
 
    
    display.blit(picture, (0, 0))
    greeting = 'Press Start for free play'
    font_process(60, greeting, white, image_centerx, 200)
    greeting = 'or'
    font_process(60, greeting, white, image_centerx, 280)
    greeting = 'Make a Donation and get a chance to win a Bonehenge Prize'
    font_process(60, greeting, white, image_centerx, 360)
    greeting = 'Prizes are awarded randomly and are not dependent on final quiz score'
    font_process(30, greeting, white, image_centerx, 800)
    greeting = 'Odds of winning are 1 in '+ str(int(100 / payout))
    font_process(30, greeting, white, image_centerx, 850)
    pygame.display.flip()
    
    # Select if this is a paid or free play
    while GPIO.input(portList2[1]) == GPIO.HIGH and GPIO.input(portList2[2]) == GPIO.HIGH:
        sleep(.05)
        #print('in pay detection')
        if GPIO.input(portList2[1]) == GPIO.LOW:
            sleep(.08)
            free = True
            win = False
            print('Free Play')
                
        if GPIO.input(portList2[2]) == GPIO.LOW:
            print('PLAYBACK SHOULD HAPPEN')
            sleep(.08)
            free = False
            win = False # set it false for now
            Rnd_Chance = int(random() * 100 )
            play_sound('Yay.mp3', .3)
            
            
            if Rnd_Chance <= payout:
                win = True
                print('A Winner')
                
            else:
                win = False
                print('A Loser')
            
def game1_intro():
    white = (255, 255, 255)
    black = (0, 0, 0,)
    red = (255, 50, 50)
    display.blit(bg_dol, (0, 0))
    greeting = 'Hello Welcome to ID the Dolphin'
    font_process(60, greeting, white, image_centerx, 100)
    pygame.display.flip()
    sleep(2)

    info = 'We can identify individuals by their dorsal fin shape'
    font_process(50, info, white, image_centerx, 200)
    #pygame.display.flip()
    # sleep(.5)

    inst = 'See if you can match one on the bottom row to the top picture'
    font_process(50, inst, white, image_centerx, 300)
    pygame.display.flip()
    if not free:
        sleep(2) # allow prev sound to end
    play_sound('pinball-start.mp3', .5)
    sleep(5.5)
    display.blit(bg_dol, (0, 0))
    pygame.display.flip()


def font_process(size, message, color, x, y):
    # attempt to combine all font operations into one call that
    # renders and blits the text
    
    black = (0,0,0)
    d_shadow = 3
    # create a font object from a system font
    font = pygame.font.SysFont('FreeSans', size, True, False)
    # render font on a new surface font.render(text, antialias, bkgnd = none)
    render_message = font.render(message, True, color)
    # render drop shadow in black
    if d_shadow:
        render_ds = font.render(message, True, black)
        render_ds_rect = render_message.get_rect()
    # attempt to center works
    # create a rectangular object for the text surface object
    render_msg_rect = render_message.get_rect()
    
    # center in x, use y from call
    #render_msg_rect.center = (image_centerx, y) # (x,y) x = screen center
    render_msg_rect.center = (x, y) # (x,y) x = screen center
    # blit drop shadow then text to image
    if d_shadow:
        #render_ds_rect.center = (image_centerx + d_shadow, y + d_shadow)
        render_ds_rect.center = (x + d_shadow, y + d_shadow)
        display.blit(render_ds, render_ds_rect)
    display.blit(render_message, render_msg_rect)
    # no flip here up to the caller

def play_sound(sfile, vol):
    pygame.mixer.music.set_volume(vol)
    pygame.mixer.music.load(gpath + sfile)
    pygame.mixer.music.play()

# ------------------------- Where all the action happens --------------
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
    GPIO.output(portList3[2], True) # turn on the button lights


    # ========= Loop Start ============
    for items in rnums:
        shuffle_pics()
        display_pic = display_pics[turn]  # picks a new one each turn
        caption = 'Turn Number ' + str(turn + 1)
        send_to_screen(display_pic, rnums, caption)  # put up the challenge screen

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
        font_process(60, score_msg, white, image_centerx, 500)
        font_process(60, pgm_rsp, white, image_centerx, 600)
        pygame.display.flip()
        turn = turn + 1
        
        sleep(1)
        # now display just the turn and score no response
        if turn != 5:
            display.blit(bg_dol, (0, 0))
            font_process(60, score_msg, white, image_centerx, 500)
            pygame.display.flip()
    # =========== Loop End =============  
      

    # final score
    score_msg = ('Final Score  '+ str(right_ans)+ ' right  '+ str(wrong_ans)+' wrong')
    final_msg = (final_resp[right_ans])
    display.blit(bg_dol, (0, 0))
    font_process(60, score_msg, white, image_centerx, 400)
    font_process(60, final_msg, white, image_centerx, 500)
    sleep(1)
    if win:
        font_process(75,'You are a WINNER!!',red, image_centerx, 600)
        font_process(75,'Please see one of our Staff for your prize',red, image_centerx, 700)
        play_sound('fanfare.mp3', 1)
        GPIO.output(portList3[1], True) # turn on the bell
        sleep(1)
        GPIO.output(portList3[1], False) # turn it off

    
    if not win and not free:
        font_process(60,'Sorry, you are not a winner this time', blue, image_centerx, 600)

    pygame.display.flip()
    GPIO.output(portList3[2], False) # turn off the button lights

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
        for index in range(1, len(portList)):
            #sleep(.03) # debounce time
            if GPIO.input(portList[index]) == GPIO.LOW:
                ans = portList[index] # first pull the value
                ans = portList.index(portList[index]) -1 # then locate it in the list
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
    display.blit(comp_pic[display_me],(840,40)) # Challange pic location
    # display the other pictures from list on bottom
    choicesx = 50
    choicesy = 700
    i = 0
    font_process(60, caption, (255,255,255), image_centerx, 400)
    #print('send to screen has rnums as ', str(rnums))
    for items in rnums:
        # use the rnums list to index your_pic list to get the pictures
        display.blit(your_pic[rnums[i]],(choicesx, choicesy))
        i = i + 1
        choicesx = choicesx + 380 # spacing for choices pics


    pygame.display.flip()

def which_game():
    ''' puts up select screen and sets game1 T or F'''
    # needs to light only buttons 1 & 5
    global game1
    print('which game will it be? ')
    display.blit(bg_dol, (0, 0))
    greeting = 'Select a game to play'
    font_process(60, greeting, white, 100, 200)
    greeting = 'ID the Dolphin'
    font_process(60, greeting, white, 10, 400)
    pygame.display.flip()
    
    while GPIO.input(portList[1]) == GPIO.HIGH and GPIO.input(portList[5]) == GPIO.HIGH:
        # wait for button press
        sleep(.05)
        if GPIO.input(portList[1]) == GPIO.LOW:
            game1 = True
        if GPIO.input(portList[5]) == GPIO.LOW:
            game1 = False
        


# ------------------- GAME 2 CODE START --------------------------
# ----------- START GAME TWO CODE --------------
def get_file(list_file):
    global row_count
    global file_error
    try:
        ''' call with file and get back list of lists'''
        with open(list_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            rowlist = []
            questions_list = []
            line_count = 0
            for row in csv_reader:
                if line_count > 0:
                    # avoids the header line
                    rowlist = [row[0]] # initalizes the list
                    rowlist.append(row[1])
                    rowlist.append(row[2])
                    rowlist.append(row[3])
                    questions_list.append(rowlist)
                    # this is a 0 based list of lists
                    # access questions_list[q# - 1][column]
                line_count += 1
            print(f'Processed {line_count} lines.')
            row_count = line_count - 1
            return [questions_list]
    except FileNotFoundError:
        print('qna_pool.csv data file not found')
        # print message on screen
        file_error = True
        


def pick_some(qpicks,rstart,rend):
    '''takes a number and returns list of randoms nums in a range'''
    pics_list = random.sample(range(rstart, rend), qpicks)
    return [pics_list]     

def q_to_screen(rand_pick, questions):
    ''' gets the next question as a list and 
    moves answers around, gets called each turn'''
    this_one = questions[rand_pick]
    # randomize the next three and assign to buttons
    #print('this one in q to scrn ' + str(this_one))
    # this gives us a scramble list
    screen_order = random.sample(range(1,4),3)
    # a list like [1,2,3] or [3,1,2] that orders the answers
    # put screen stuff together with font_process
    return screen_order


def get_user_ans(rand_pic, right_ans, questions, screen_order):
    ''' matches user input to correct answer '''
    #print('get usr ans has ' + str(right_ans))
    # display stuff
    print('Question is ' + str(questions[rand_pic][0]))
    # now display the reorderd choices
    # the index below questions is the big list then
    # [rand_pic] pics which of the questions and
    # [screen_order[X]] points the the reordered answers
    print('Left 1 =' + str(questions[rand_pic][screen_order[0]]))
    print('Mid 2 =' + str(questions[rand_pic][screen_order[1]]))
    print('Rgt 3 =' + str(questions[rand_pic][screen_order[2]]))
    user_ans = input('Select 1-3 ')
    # code below to be replaced with button input
    if int(user_ans) == right_ans:
        correct = True
    else:
        correct = False
    return correct

def take_turns():
    right_count = 0
    
    for turn_no in range(0,5):
        # put up the questions
        rand_pic = q_pics[0][turn_no]
        # rand_pic points to the index of the question 0 to row_count -1
        screen_order = q_to_screen(rand_pic, questions)
        right_ans = screen_order.index(1) + 1
        #print('back with this order ' + str(screen_order))
        #print('right answer is in position '+ str(right_ans))
        # go get answers lots of stuff in this call but it needs
        # all of it
        correct = get_user_ans(rand_pic, right_ans, questions, screen_order)
        if correct:
            print('got it')
            right_count += 1
        else:
            print('no such luck')
    return right_count        

def donation_start():
    pass

def free_start():
    pass

# ----------- END GAME 2 CODE ----------------

# -------------------  GAME 2 CODE END ---------------------------


# METHODS AND FUNCTIONS END _________________________________________
# ///////////////////////////////////////////////////////////////////


# INITIALIZE RUN ONCE CODE START ------------------------------------
#region
pygame.init()
pygame.mixer.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'
clock = pygame.time.Clock()
screen_width = 1920
screen_height = 1080
bgColor = (0,0,0)
size = (screen_width, screen_height)

# assign I/O ports
portassign(portList) # main buttons
portassign(portList2) # free or pay
portassign(portList3) # output for bell and lights relays
GPIO.output(portList3[1], False) # no bell
GPIO.output(portList3[2], False) # no lights

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
g2_open_pict = gpath + 'g2_open_bkg.jpg'
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
g2_open_bkg = pygame.image.load(g2_open_pict).convert_alpha()

# these lists point to the picture files, there are 5 matching pairs
# currently they are the same pictures but will be replaced
#endregion
# game 2 run once ------------------------
try:
    [questions] = get_file(list_file)
except:
    print('FILE IS MISSING')
    #once this is inside a loop ADD BREAK 
    

print('there are ' + str(row_count) + ' rows')
# pick 5 questions out of how many are in file
# this is a list of questions to be asked
# just need to do it once per game
q_pics = pick_some(5, 0, row_count -1)
# whatever is in the 1 slot is correct pick
turn_no = 0
# game 2 run once end --------------------


# INITIALIZE RUN ONCE CODE END _________________________________________

# ************************ MAIN START **********************************

def main():
    try:
        init()
        main_loop = True
        global game1
        # note init only runs once
        
        while main_loop:
            which_game()
            if game1:
                print('game one picked')
                
                print('Main Program')
                show_rules(bg_dol)
                game1_intro()
                shuffle_pics()
                play_loop() # this is where all the work is done might want to break it up
                
            

            else:
                print('picked game 2')
            
                # make it go
                # at start donation or free play?
                show_rules(g2_open_bkg)
                if donation:
                    donation_start()
                else:
                    free_start()
                final_score = take_turns()
                print('Your final score is '+str(final_score)+' right and '+str(5 -final_score)+ ' wrong')
            
            


    except KeyboardInterrupt:
        #cleanup at end of program
        print('   Shutdown')
        GPIO.cleanup()

if __name__ == '__main__':
    main()