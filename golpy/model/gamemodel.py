from model.field import Field
from model.rules.baserule import BaseRule
from model.rules.lifeRules import LifeRule
from model.rules.generationsRule import GenerationsRule

import re  # Used to determine type of rule


class GameModel:
    def __init__(self, rule: str="3/23", field_size=(100, 100), num_generations: int = 1000):
        self.field = Field(size=field_size)
        self.rule = BaseRule()
        self.num_generations = num_generations
        self.update_rule(rule)

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
        
    def run(self):
        for _ in range(self.num_generations):
            self.update_field()
