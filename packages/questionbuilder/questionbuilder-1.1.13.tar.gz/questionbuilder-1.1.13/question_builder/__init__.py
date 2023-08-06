from question_builder.config import config

VERSION_FILE_PATH = config.PACKAGE_ROOT / "VERSION"


with open(VERSION_FILE_PATH) as file:
    __version__ = file.read().strip()
