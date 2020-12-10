import golpy.model.gamemodel as model
from golpy.eventmanager.eventmanager import *
from golpy.model.statemachine import *

import pygame

class Controller():
    """ Controls Input from Keyboard and Mouse """
    def __init__(self, event_manager, game_model):
        self.event_manager = event_manager
        event_manager.register_listener(self)
        self.game_model = game_model

    def notify(self, event):
        """ Receive events posted to the message queue """
        if isinstance(event, TickEvent):                # Called for each game tick. We check our keyboard presses here.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:           # handle window manager closing our window
                    self.event_manager.Post(QuitEvent())
                    self.event_manager.unregister_listener(self)
                if event.type == pygame.KEYDOWN:        # handle key down events
                    if event.key == pygame.K_ESCAPE:
                        self.event_manager.Post(StateChangeEvent(None))
                    else:
                        currentstate = self.game_model.state.peek()
                        if currentstate == STATE_PLAY:
                            self.keydownplay(event)
                        if currentstate == STATE_PAUSE:
                            self.keydownpause(event)
                if event.type == pygame.MOUSEBUTTONDOWN:# handle mouse click events
                    #TODO - Add behaviour for mouse-clicks
                    pass


    def keydownpause(self, event):
        """ Handles pause key events """
        #TODO - Look at this stuff right here....
        # space, enter or escape pops help
        if event.key in [pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN]:
            self.event_manager.Post(StateChangeEvent(None))

    def keydownplay(self, event):
        """ Handles play key events """
        #TODO - Look at this stuff right here....
        if event.key == pygame.K_ESCAPE:
            self.event_manager.Post(StateChangeEvent(None))
        # F1 shows the help
        if event.key == pygame.K_SPACE:
            self.event_manager.Post(StateChangeEvent(STATE_PAUSE))
        else:
            self.event_manager.Post(InputEvent(event.unicode, None))
