import model.gamemodel as model
import config
import argparse


def pass_args():
    """ Takes Argument from the command line and returns an ArgumentParser"""
    parser = argparse.ArgumentParser(description="2D Cellular Automata Viewer supporting multiple formats")
    parser.add_argument("-rule", "-r", type=str, default=config.default_rule,
                        help='String describing the used rule')
    parser.add_argument("-size", "-s", type=int, default=config.default_size,
                        help="Integer describing size of the universe. I.e. -size 200 will correspond to a (200 x 200) cell universe")
    return parser.parse_args()


def run():
    args = pass_args()
    game_model = model.GameModel(rule=args.rule, 
                                 field_size=(args.size, args.size),
                                 num_generations=1000)
    game_model.run()


if __name__ == '__main__':
    run()
