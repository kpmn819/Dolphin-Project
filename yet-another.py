import csv
import random

list_file = 'qna_pool.csv'
file_error = False
row_count = 0
donation = False

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

# ------------ START RUN ONCE ---------
# get the list of the list of all questions
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
# ------ END RUN ONCE --------------

# make it go
# at start donation or free play?
if donation:
    donation_start()
else:
    free_start()
final_score = take_turns()
print('Your final score is '+str(final_score)+' right and '+str(5 -final_score)+ ' wrong')