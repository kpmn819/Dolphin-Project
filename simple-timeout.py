
import timeout_decorator


@timeout_decorator.timeout(5,use_signals=True)
def delay_1():
    first = input('Waiting on delay_1 ')
    return first


def delay_2():
    second = input('Waiting on delay_2 ')
    return second


def delay_3():
    third = input('Waiting on delay_3 ')
    return third


def main():
    try:
        try:
            num1 = delay_1()
            print('back from 1 with' + num1)
        except:
            print('here we are')

        num2 = delay_2()
        print('back from delay_2 ' + num2)
                
    

    except KeyboardInterrupt:
        #cleanup at end of program
        print('   Shutdown')
        

if __name__ == '__main__':
    main()