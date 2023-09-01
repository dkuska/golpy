from model.field import Field
from model.rules.baserule import BaseRule
from model.rules.lifeRules import LifeRule
from model.rules.generationsRule import GenerationsRule
from stats import Statistics


import re  # Used to determine type of rule


class GameModel:
    def __init__(self, rule: str="3/23", field_size=(100, 100), num_generations: int = 1000, stats_folder: str = ""):
        self.field = Field(size=field_size)
        self.rule = BaseRule()
        self.num_generations = num_generations
        self.update_rule(rule)
        
        self.stats_folder = stats_folder
        self.statistics = Statistics()

    def reset_rule(self):
        """ Reset rule to be a blank baserule"""
        self.rule = BaseRule()

    def update_rule(self, rule_str):
        """ Checks the rule_str with regex to determine type of rule and creates new rule object"""
        life_regex = re.match("[0-9]*/[0-9]*", rule_str)
        life_alt_regex = re.match("B[0-9]*/S[0-9]*", rule_str)
        generations_regex = re.match("[0-9]*/[0-9]*/[0-9]*", rule_str)
        generations_alt_regex = re.match("B[0-9]*/S[0-9]*/[0-9]+", rule_str)

        if generations_regex or generations_alt_regex:
            self.rule = GenerationsRule(rule_str)
        else:
            if life_regex or life_alt_regex:
                self.rule = LifeRule(rule_str)
            else:
                self.rule = BaseRule(rule_str)

    def run(self):
        for i in range(self.num_generations):
            old_field = self.field.cells.copy() # Create copy of old field for statistics
            self.field.update(self.rule)
            self.statistics.collect_generation_stats(generation=i, old_field=old_field, new_field=self.field.cells)
            
            print(self.field.cells)  # DEBUG
        
        self.statistics.save_statistics(self.stats_folder)