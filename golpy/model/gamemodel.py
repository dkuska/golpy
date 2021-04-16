from golpy.model.field import Field
from golpy.model.rules.baserule import BaseRule
from golpy.model.rules.lifeRules import LifeRule
from golpy.model.rules.generationsRule import GenerationsRule
from golpy.model.statemachine import *
from golpy.eventmanager.eventmanager import *

import re  # Used to determine type of rule


class GameModel:
    def __init__(self, event_manager, rule_str="3/23", field_size=(100, 100)):
        # MVC Logic
        self.event_manager = event_manager
        event_manager.register_listener(self)
        self.running = False
        self.state = StateMachine()

        # Cellular Automata Logic
        # Playing Field
        self.field = Field(size=field_size)
        # Rule
        self.rule = BaseRule()
        self.update_rule(rule_str)

    def reset_rule(self):
        """ Reset rule to be a blank baserule"""
        self.rule = BaseRule()

    def update_rule(self, rule_str):
        """ Checks the rule_str with regex to determine type of rule and creates new rule object"""
        life_regex = re.match("[0-9]*/[0-9]*", rule_str)
        life_alt_regex = re.match("B[0-9]*/S[0-9]*", rule_str)
        generations_regex = re.match("[0-9]*/[0-9]*/[0-9]*", rule_str)
        generations_alt_regex = re.match("B[0-9]*/S[0-9]*/[0-9]+", rule_str)

        # USEFUL IN THE FUTURE WHEN LTL-RULES ARE ALLOWED
        #ltl_regex = re.match("",rule_str)
        #ltl_alt_regex = re.match("", rule_str)

        if generations_regex or generations_alt_regex:
            self.rule = GenerationsRule(rule_str)
        else:
            if life_regex or life_alt_regex:
                self.rule = LifeRule(rule_str)
            else:
                self.rule = BaseRule(rule_str)

    def update_field(self):
        """ Gives notice to field to update itself according to the current rule"""
        self.field.update(self.rule)

    ### INTERACTION WITH EVENTMANAGER, MAIN LOOP
    def notify(self, event):
        """ Called by an event in the message queue """
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
