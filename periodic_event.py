# coding=utf-8

# imports the Pygame library
import pygame


def main():
    # initializes Pygame
    pygame.init()

    # sets the window title
    pygame.display.set_caption(u'Periodic event')

    # sets the window size
    pygame.display.set_mode((400, 400))

    # creates two custom events
    CUSTOMEVENT_1 = pygame.USEREVENT
    CUSTOMEVENT_2 = pygame.USEREVENT + 1

    # inserts two custom events into the event queue
    pygame.time.set_timer(CUSTOMEVENT_1, 100)
    pygame.time.set_timer(CUSTOMEVENT_2, 200)

    # is the application running?
    is_running = True

    # if the application is running
    while is_running:
        # gets events from the event queue
        for event in pygame.event.get():
            # if the 'close' button of the window is pressed
            if event.type == pygame.QUIT:
                # stops the application
                is_running = False

            # captures the custom event 'CUSTOMEVENT_1'
            if event.type == CUSTOMEVENT_1:
                # prints on the console that 'CUSTOMEVENT_1' has been captured and the capture time
                print(u'custom event "CUSTOMEVENT_1" captured ({} ms)'.format(pygame.time.get_ticks()))

            # captures the custom event 'CUSTOMEVENT_2'
            if event.type == CUSTOMEVENT_2:
                # prints on the console that 'CUSTOMEVENT_2' has been captured and the capture time
                print(u'custom event "CUSTOMEVENT_2" captured ({} ms)'.format(pygame.time.get_ticks()))

    # finalizes Pygame
    pygame.quit()


if __name__ == '__main__':
    main()