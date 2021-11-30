# coding=utf-8

# imports the Pygame library
import pygame


def main():
    # initializes Pygame
    pygame.init()

    # sets the window title
    pygame.display.set_caption('Mouse events')

    # sets the window size
    pygame.display.set_mode((400, 400))

    # infinite loop
    while True:
        # gets a single event from the event queue
        event = pygame.event.wait()

        # if the 'close' button of the window is pressed
        if event.type == pygame.QUIT:
            # stops the application
            break

        # if any mouse button is pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            print('Button Down')
            # prints on the console the pressed button and its position at that moment
            #print u'button {} pressed in the position {}'.format(event.button, event.pos)
            print(str(event.pos))

        # if any mouse button is released
        if event.type == pygame.MOUSEBUTTONUP:
            print('Button Up')
            # prints on the console the button released and its position at that moment
            print(str(event.pos))

        # if the mouse is moved
        if event.type == pygame.MOUSEMOTION:
            print('Motion')
            # prints on the console the pressed buttons, and their position and relative movement at that time
            print(str(event.pos))


    # finalizes Pygame
    pygame.quit()


if __name__ == '__main__':
    main()