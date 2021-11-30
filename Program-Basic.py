#!/usr/bin/python3


# IMPORTS START --------------------------------------------------

# IMPORTS END ____________________________________________________

# VARIABLE INITIALIZE START----------------------------------------
max_pic = 5

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
def get_rnd:
    # uses max_pic to get a random number
    pass
def show_rules:
    # display rules and wait for input
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
            

    except KeyboardInterrupt:
        #cleanup at end of program
        print('   Shutdown')
        GPIO.cleanup()    

if __name__ == '__main__':
    main()

