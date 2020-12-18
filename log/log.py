import logging

class Logger(logging.Logger):

    def __init__(self, output = "console"):
        self.output = output

    def log_to_console(self, message):
        self.log(message)

