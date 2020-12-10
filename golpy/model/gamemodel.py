from golpy.model.field import Field
from golpy.model.rules.baserule import BaseRule
from golpy.model.rules.lifeRules import LifeRule
from golpy.model.statemachine import *
from golpy.eventmanager.eventmanager import *

import re


class GameModel():
    def __init__(self, event_manager):
        # MVC Logic
        self.event_manager = event_manager
        event_manager.register_listener(self)
        self.running = False
        self.state = StateMachine()

        # GOL Logic
        self.field = Field(size=100, rule_str="3/23")
        self.rule = BaseRule()
        self.update_rule("3/23")

    def update_rule(self, rule_str):
        # TODO - add regex to determine type of rule
        lifeRegex = re.match("[0-9]+\/[0-9]+", rule_str)
        if lifeRegex:
            self.rule = LifeRule(rule_str)
        else:
            self.rule = LifeRule(rule_str)


    def update_field(self):
        #TODO - implement application of rule to field
        pass

    def notify(self, event):
        """ Called by an event in the message queue """
        #TODO - Check which Events the Model should react to
        if isinstance(event, QuitEvent):
            self.running = False
        if isinstance(event, StateChangeEvent): #TODO - Check whatever this is useful for....
            # pop request
            if not event.state:
                # false if no more states are left
                if not self.state.pop():
                    self.event_manager.Post(QuitEvent())
            else:
                # push a new state on the stack
                self.state.push(event.state)

    def run(self):
        """ Starts the game engine loop.
        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify() """
        self.running = True
        self.event_manager.Post(InitializeEvent())
        self.state.push(STATE_PLAY)
        while self.running:
            new_tick = TickEvent()
            self.event_manager.Post(new_tick)
