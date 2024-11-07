import logging


class Logger:
    def __init__(self, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                 decorated=False, log_file='app.log'):
        self.decorated = decorated
        self.log_file = log_file
        self._setup_logging(level, format)

    def _setup_logging(self, level, format):
        # Remove todos os handlers existentes
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        logging.basicConfig(level=level, format=format)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(logging.Formatter(format))
        logging.getLogger().addHandler(console_handler)

        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.ERROR)
        file_handler.setFormatter(logging.Formatter(format))
        logging.getLogger().addHandler(file_handler)

    def _decorate_message(self, message):
        if self.decorated:
            return f"====== {message} ======"
        else:
            return message

    def info(self, message):
        logging.info(self._decorate_message(message))

    def error(self, message):
        logging.error(self._decorate_message(message))

    def warning(self, message):
        logging.warning(self._decorate_message(message))

    def debug(self, message):
        logging.debug(self._decorate_message(message))

    def exception(self, message):
        logging.exception(self._decorate_message(message))
