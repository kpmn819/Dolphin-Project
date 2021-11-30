#!/usr/bin/python3



from random import random
# vars
Free = False
Win = False
PayOut = 90
# what is happening
def main():
    try:
        while 1:
            waitforit = input('waiting')
            Rnd_Chance = int(random() * 100 )
            #Rnd_Chance = 95
            print('Random = ',Rnd_Chance)
            Win = False
            if Rnd_Chance >= PayOut:
                Win = True
            
                print('Winner true = ', Win)
            else:
                Win = False
                print('Winner false = ', Win)
 

    except KeyboardInterrupt:
        #cleanup at end of program
        print('   Shutdown')
        

if __name__ == '__main__':
    main()
