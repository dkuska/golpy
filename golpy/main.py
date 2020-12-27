import golpy.controller.controller as controller
import golpy.view.view as view
import golpy.model.gamemodel as model
import golpy.eventmanager.eventmanager as eventm
import log.log as log

import golpy.model.rules.example_rules as examples

import argparse


def pass_args():
    parser = argparse.ArgumentParser(description="2D Cellular Automata Viewer supporting multiple formats")
    parser.add_argument("-rule", "-r", help='String describing the used rule', type=str, default=examples.gol_generations)
    parser.add_argument("-mode", "-m",  help="String describing Game Mode", type=str, default="gol")
    parser.add_argument("-size", "-s", help="Integer describing size of the universe. I.e. -size 200 will correspond to a (200 x 200) cell universe", type=int, default=100)
    parser.add_argument("-topology", "-to", "-t", type=str, default="torus", help="String describing the topology of the universe. Default being Torus-shaped")

    return parser.parse_args()


def run():
    args = pass_args()
    logger = log.Logger()
    event_manager = eventm.EventManager()
    game_model = model.GameModel(event_manager, rule_str=args.rule, field_size=(args.size, args.size))
    game_view = view.View(event_manager, game_model, size=600, tick_rate=20)
    game_controller = controller.Controller(event_manager, game_model)

    game_model.run()


if __name__ == '__main__':
    run()
