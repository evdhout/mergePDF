import configparser
from models.options import Options


class OptionsController:
    def __init__(self):
        self.options = Options()
        self._read_ini()

    def _read_ini(self):
        config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        config.read('mergePDF.ini')

        self.options.debug = config.getboolean('DEBUG', 'debug', fallback=False)
        self.options.set_path(path=config.get('MERGEPDF', 'initial directory', fallback=None))
