import golpy.controller.controller as controller
import golpy.view.view as view
import golpy.model.gamemodel as model
import golpy.eventmanager.eventmanager as eventm

def run():
    event_manager = eventm.EventManager()
    game_model = model.GameModel(event_manager)
    game_view = view.View(event_manager, game_model, size = 800)
    game_controller = controller.Controller(event_manager, game_model)

    game_model.run()

if __name__ == '__main__':
    run()
