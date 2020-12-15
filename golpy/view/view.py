import pygame
from pygame.locals import *
import numpy as np
from PIL import Image

from golpy.eventmanager.eventmanager import *
import golpy.model.statemachine as statemachine

class View():
    """ Uses Pygame to show """
    def __init__(self, event_manager, game_model, size):
        self.event_manager = event_manager
        event_manager.register_listener(self)
        self.game_model = game_model

        self.screen = None
        self.screen_size = (0,0)
        self.clock = None
        self.size = size
        self.is_initialized = False
        self.initialize()   #TODO - Does this have to be a seperate call?

    def initialize(self):
        numpass, numfail = pygame.init()
        self.screen_size = (self.size,self.size)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        self.is_initialized = True

    def notify(self, event):
        """ Receive events posted to the message queue """
        if isinstance(event, InitializeEvent):
            self.initialize()
        elif isinstance(event, QuitEvent):
            self.is_initialized = False         # shut down the pygame graphics
            pygame.quit()
        elif isinstance(event, TickEvent):
            if not self.is_initialized:
                return
            self.game_model.field.update()      #Update playing field at each tick
            current_state = self.game_model.state.peek()
            if current_state == statemachine.STATE_MENU:
                self.render_menu()
            if current_state == statemachine.STATE_PLAY:
                self.render_play()
            # limit the redraw speed to 2 frames per second
            self.clock.tick(5)

    def render_play(self):
        """ Displays the current move on the screen, resizes Cells from Model to screensize"""
        cells = self.game_model.field.cells * 255   #TODO Change this so that different color schemes are possible
        PIL_image = Image.fromarray(np.uint8(cells)).resize((self.screen_size), resample=Image.NEAREST) #Convert np.array to PIL.Image for resizing
        img_arr = np.array(PIL_image)                   #Create numpy array from PIL_Image
        background = pygame.surfarray.make_surface(img_arr) #Create pygame surface object
        self.screen.blit(background, (0,0))             #Draws Image on Screen
        pygame.display.flip()

    def render_menu(self):
        #TODO - Add menu call
        pass
