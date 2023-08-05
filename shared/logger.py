import logging


class Logger:
    def __init__(self, level=logging.INFO):
        self.logger = logging.getLogger('stdout_logger')
        self.logger.setLevel(level)
        formatter = logging.Formatter(
            '[%(levelname)s] %(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def info(self, module, message):
        self.logger.info(f'[{module}] {message}')


logger = Logger()
