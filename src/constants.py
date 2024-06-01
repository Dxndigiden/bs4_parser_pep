from pathlib import Path


MAIN_DOC_URL = 'https://docs.python.org/3/'
BASE_DIR = Path(__file__).parent
DT_FORMAT_FOR_FILE = '%Y-%m-%d_%H-%M-%S'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT_FOR_LOG = '%d.%m.%Y %H:%M:%S'
MAIN_PEPS_URL = 'https://peps.python.org/'
EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
PRETTY_OUTPUT = 'pretty'
FILE_OUTPUT = 'file'
LOG_DIR = 'logs'
LOG_FILE = 'parser.log'
DOWNLOADS_DIR = 'downloads'
