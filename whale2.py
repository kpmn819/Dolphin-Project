#!/usr/bin/python3


# IMPORTS START --------------------------------------------------
from random import randrange, shuffle
from time import sleep

# IMPORTS END ____________________________________________________

# VARIABLE INITIALIZE START----------------------------------------
max_pic = 5
rnums = []
display_pic = 0
resp = 0
# these lists point to the picture files, there are 5 matching pairs
# currently they are the same pictures but will be replaced
your_pic = ['whale1.jpg', 'whale2.jpg', 'whale3.jpg', 'whale4.jpg', 'whale5.jpg']
comp_pic = ['1whale1.jpg', '2whale2.jpg', '3whale3.jpg', '4whale4.jpg', '5whale5.jpg']


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

    display_pic = randrange(max_pic)
    print('selected picture ' + str(randrange(max_pic)))
    rnums = [x for x in range(max_pic)]
    shuffle(rnums)
    print(rnums)



    # iterate to build a list of random numbers
    pass
def show_rules():
    # display rules and wait for input
    x=input('Here are the rules, press any key')

def play_loop():
    pos_resp=['Correct','Got it, Nice','Right','Good Pick','Way to go','On a roll']
    neg_resp=['Sorry','Nope','Not that one','Too bad','Gotcha','Maybe next time']
    final_resp=['Better Try Again','Keep Working at it','Not Bad','Pretty Good','Excellent Nice JOb','100% Wow!']
    right_ans = 0
    wrong_ans = 0
    # use display_pic to put up that pic on left
    # use rnums to show all pics on right
    for items in rnums:
        shuffle_pics()
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
    # final score
    print(final_resp[right_ans])
    # add delay here
    sleep(5)
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
