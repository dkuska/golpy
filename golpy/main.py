import golpy.controller.controller as controller
import golpy.view.view as view
import golpy.model.gamemodel as model
import golpy.eventmanager.eventmanager as eventm
import log.log as log

import golpy.model.rules.example_rules as examples


def run():
    logger = log.Logger()
    event_manager = eventm.EventManager()
    game_model = model.GameModel(event_manager, rule_str=examples.replicator, field_size=(150,150))
    game_view = view.View(event_manager, game_model, size=600, tick_rate=20)
    game_controller = controller.Controller(event_manager, game_model)

    game_model.run()


if __name__ == '__main__':
    run()
