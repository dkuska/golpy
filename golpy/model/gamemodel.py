from golpy.model.field import Field
from golpy.model.rules.baserule import BaseRule
from golpy.model.rules.lifeRules import LifeRule
from golpy.model.statemachine import *
from golpy.eventmanager.eventmanager import *

import re  # Used to determine type of rule

class GameModel():
    def __init__(self, event_manager, rule_str="3/23"):
        # MVC Logic
        self.event_manager = event_manager
        event_manager.register_listener(self)
        self.running = False
        self.state = StateMachine()

        # Cellular Automata Logic
        # Playing Field
        self.field = self.create_field();
        # Rule
        self.rule = BaseRule()
        self.update_rule(rule_str)

    def reset_rule(self):
        self.rule = BaseRule()

    def update_rule(self, rule_str):
        # TODO - add regex to determine type of rule
        lifeRegex = re.match("[0-9]+\/[0-9]+", rule_str)
        if lifeRegex:
            self.rule = LifeRule(rule_str)
        else:
            self.rule = LifeRule(rule_str)

    def create_field(self, size=None, mode='default', neighborhood='M', bounded=True):
        field = Field(size=size, mode=mode, neighborhood=neighborhood, bounded=bounded)
        return field

    def update_field(self):
        self.field.update(self.rule)

    def notify(self, event):
        """ Called by an event in the message queue """
        # TODO - Check which Events the Model should react to
        if isinstance(event, QuitEvent):
            # Clean up data
            self.running = False
        if isinstance(event, StateChangeEvent):  # TODO - Check whatever this is useful for....
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
