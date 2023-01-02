from pathlib import Path
import platform


class Options:
    APPLICATION_NAME: str = "MergePDF"
    APPLICATION_AUTHOR: str = "evdhout"
    APPLICATION_AUTHOR_URL: str = "https://github.com/evdhout"
    APPLICATION_VERSION: str = "december 2022"
    APPLICATION_SOURCE_URL: str = "https://github.com/evdhout/mergePDF"

    WINDOWS: str = 'Windows'
    LINUX: str = 'Linux'
    MACOS: str = 'Darwin'

    def __init__(self):
        self.debug: bool = False
        self.path: Path or None = None
        self.os: str = platform.system()

    def get(self, option: str, default: None):
        value = getattr(self, option, None)
        if value is None:
            return default
        else:
            return value

    def set_path(self, path: str or None):
        if path is not None:
            self.path = Path(path).expanduser()
            if not self.path.is_dir():
                raise FileExistsError(f'Path {self.path} is not a valid directory.')

    def message(self, message: str, end: str = '\n'):
        if self.debug:
            print(message, end=end)

    def is_windows(self) -> bool:
        return self.os == Options.WINDOWS

    def is_linux(self) -> bool:
        return self.os == Options.LINUX

    def is_macos(self) -> bool:
        return self.os == Options.MACOS
