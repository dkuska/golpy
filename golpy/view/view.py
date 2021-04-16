import pygame
import numpy as np
from PIL import Image

from golpy.eventmanager.eventmanager import *
import golpy.model.statemachine as statemachine

from golpy.config import *


class View:
    def __init__(self, event_manager, game_model, size=0, tick_rate=30, save_img=True):
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

        self.save_img = save_img  # Boolean used to determine if image should be saved
        self.images = []
        self.image_counter = 0
        self.save_str = default_save_path  # TODO - Make this not hardcoded

    def initialize(self):
        """ Initializes Pygame components, gets called through eventmanager-queue"""
        numpass, numfail = pygame.init()
        if numfail > 0:
            print("Error initializing Pygame")
            # TODO - Logging

        pygame.display.set_caption("golpy - 2D cellular automata simulation")
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

        if self.save_img:  # If flag is set, save a png of the image
            self.save_field(pil_image)

        background = pygame.surfarray.make_surface(img_arr)  # Create pygame surface object
        self.screen.blit(background, (0, 0))  # Draws Image on Screen
        pygame.display.flip()

    def save_field(self, pil_img):
        """ Saves an img into the img folder"""
        if self.image_counter < 100:  # TODO - Determine how large the gifs should become
            self.image_counter += 1
            self.images.append(pil_img)  # Append current image to image_array (useful, when saving animation as gif=
            save_string = self.save_str + default_rule.replace("/", "") + "_" + str(self.image_counter) + ".png"  # TODO - Make file path not hardcoded
            pil_img.save(fp=save_string, format="PNG")

    def save_as_gif(self):
        """ Creates a gif file from the images"""
        out = self.save_str + default_rule.replace("/", "") + ".gif"
        self.images[0].save(out, save_all=True, append_images=self.images[1:], duration=200, loop=0)

    ### MVC Logic
    def notify(self, event):
        """ Receive events posted to the message queue """
        if isinstance(event, InitializeEvent):
            self.initialize()
        elif isinstance(event, QuitEvent):
            if self.save_img:
                self.save_as_gif()
            self.is_initialized = False  # shut down the pygame graphics
            pygame.quit()
        elif isinstance(event, TickEvent):
            if self.is_initialized:  # Ignore Tick- Events if the view is not initialized
                self.game_model.update_field()  # Update playing field at each tick
                current_state = self.game_model.state.peek()
                if current_state == statemachine.STATE_MENU:
                    pass  # TODO - ADD Menu
                if current_state == statemachine.STATE_PLAY:
                    self.render_play()
                if current_state == statemachine.STATE_PAUSE:
                    pass
