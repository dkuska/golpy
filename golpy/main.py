import controller.controller as controller
import view.view as view
import model.gamemodel as model
import eventmanager.eventmanager as eventm
import config
import argparse


def pass_args():
    """ Takes Argument from the command line and returns an ArgumentParser"""
    parser = argparse.ArgumentParser(description="2D Cellular Automata Viewer supporting multiple formats")
    parser.add_argument("-rule", "-r", type=str, default=config.default_rule,
                        help='String describing the used rule')
    parser.add_argument("-mode", "-m", type=str, default=config.default_mode,
                        help="String describing Game Mode")
    parser.add_argument("-size", "-s", type=int, default=config.default_size,
                        help="Integer describing size of the universe. I.e. -size 200 will correspond to a (200 x 200) cell universe")
    parser.add_argument("-topology", "-t", type=str, default=config.default_topology,
                        help="String describing the topology of the universe. Default being Torus-shaped")
    parser.add_argument("-speed", "-sp", type=int, default=config.default_speed,
                        help="Integer describing the maximum FPS possible for the animation")
    parser.add_argument("-windowsize", "-w", type=int, default=config.default_window_size,
                        help="Integer describing the window size in pixels")
    parser.add_argument("-save", "-sa", type=int, default=config.default_save,
                        help="Integer describing if images should be saved to the img folder. 0 - don't save, 1 - save")
    parser.add_argument("-start", "-st", type=str, default=config.default_starting_config,
                        help="String specifying the starting configuration of the universe. Currently supported: soup, glider. Default: soup")


    return parser.parse_args()


def run():
    args = pass_args()
    event_manager = eventm.EventManager()
    game_model = model.GameModel(event_manager, rule_str=args.rule, field_size=(args.size, args.size))
    game_view = view.View(event_manager, game_model, size=args.windowsize, tick_rate=args.speed)
    game_controller = controller.Controller(event_manager, game_model)
    game_model.run()


if __name__ == '__main__':
    run()
