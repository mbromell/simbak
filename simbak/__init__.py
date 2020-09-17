import logging as _logging
import logging.handlers as _handlers
import os as _os

from simbak.agent.normal import NormalAgent as _NormalAgent

__version__ = '0.2.0'

# Setting up logger files
log_path = './simbak.log'

# Windows
if _os.name == 'nt':
    appdata = _os.getenv('APPDATA')
    log_path = _os.path.join(appdata, 'simbak')
# Linux
elif _os.name == 'posix':
    log_path = _os.path.join('var', 'log', 'simbak')

if _os.path.exists(log_path) is False:
    _os.mkdir(log_path)

# Setting up the format of the logs.
_stream_formatter = _logging.Formatter('%(levelname)s: %(message)s')
rotating_file_formatter = _logging.Formatter(
    fmt='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d, %H-%M-%S'
)

# Stream handler for logging to the terminal.
_stream_handler = _logging.StreamHandler()
_stream_handler.setLevel(_logging.INFO)
_stream_handler.setFormatter(_stream_formatter)

# File handler for logging to a file.
_rotating_file_handler = _handlers.RotatingFileHandler(
    _os.path.join(log_path, 'simbak.log'), maxBytes=1000000, backupCount=20)
_rotating_file_handler.setLevel(_logging.DEBUG)
_rotating_file_handler.setFormatter(rotating_file_formatter)

_root_logger = _logging.getLogger()
_root_logger.setLevel(_logging.DEBUG)
_root_logger.addHandler(_stream_handler)
_root_logger.addHandler(_rotating_file_handler)


def backup(sources: list, destinations: list, name: str,
           compression_level: int = 6):
    """The easiest way to perform a standard backup.

    Args:
        sources (list of str): Paths to the files that you are backing
            up.
        destinations (list of str): Paths of where you want the backup
            to be stored.
        name (str): Name of the backup, this will name the backup files.
        compression_level (int, optional): The gzip compression level
            that you want to use for the backup. Defaults to 6.
    """
    agent = _NormalAgent(sources, destinations, name, compression_level)
    agent.backup()
