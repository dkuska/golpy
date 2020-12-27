import pygame
import numpy as np
from PIL import Image

from golpy.eventmanager.eventmanager import *
import golpy.model.statemachine as statemachine


class View():
    def __init__(self, event_manager, game_model, size=0, tick_rate=30, save_img = False):
        # MVC Logic
        self.event_manager = event_manager
        event_manager.register_listener(self)
        self.game_model = game_model

        self.screen = None
        self.screen_size = (0, 0)
        self.clock = None
        self.tick_rate = tick_rate

        self.size = size
        self.is_initialized = False

        self.save_img = save_img


    def initialize(self):
        """ Initializes Pygame components, gets called through eventmanager-queue"""
        numpass, numfail = pygame.init()
        if numfail > 0:
            print("Error initializing Pygame")
            # TODO - Logging

        pygame.display.set_caption(("golpy - 2D cellular automata simulation"))
        self.screen_size = (self.size, self.size)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        self.clock.tick(self.tick_rate)
        self.is_initialized = True

    def render_play(self):
        """ Displays the cells on the screen, resizes to screensize"""
        cells = self.game_model.field.cells * 255  # TODO Change this so that different color schemes are possible
        pil_image = Image.fromarray(np.uint8(cells)).resize(self.screen_size,
                                                            resample=Image.NEAREST)  # Convert np.array to PIL.Image for resizing
        img_arr = np.array(pil_image)  # Create numpy array from PIL_Image
        background = pygame.surfarray.make_surface(img_arr)  # Create pygame surface object
        self.screen.blit(background, (0, 0))  # Draws Image on Screen
        pygame.display.flip()

    def render_menu(self):
        """ Displays the starting menu """
        # TODO - Actually call this function
        font = pygame.font.SysFont("Times New Roman", 72)
        text = font.render("Hello Pygame")
        surface = pygame.Surface(self.screen_size, pygame.SRCALPHA)
        background = []
        self.screen.blit(background, (0, 0))
        pygame.display.flip()
        pass

    def save_field(self, pil_img):
        """ Saves an img created by PIL into the img folder"""
        pass


### MVC Logic
    def notify(self, event):
        """ Receive events posted to the message queue """
        if isinstance(event, InitializeEvent):
            self.initialize()
        elif isinstance(event, QuitEvent):
            self.is_initialized = False         # shut down the pygame graphics
            pygame.quit()
        elif isinstance(event, TickEvent):
            if self.is_initialized:             # Ignore Tick- Events if the view is not initialized
                self.game_model.update_field()  # Update playing field at each tick
                current_state = self.game_model.state.peek()
                if current_state == statemachine.STATE_MENU:
                    self.render_menu()
                if current_state == statemachine.STATE_PLAY:
                    self.render_play()
