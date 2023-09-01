""" File containing the default configuration, that's used, when the script is called without cmd args"""
import model.rules.example_rules as examples

default_rule = examples.gol
default_size = 10
default_generations = 10
default_statistics_folder = "./stats/"