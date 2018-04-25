"""
Define configuration parameters.
"""

__all__ = ['CONFIG',
           'setup_logging',
           'setup_conf_user'
          ]

import sys
import os
import json
import logging
from pkg_resources import Requirement, resource_filename

from climada.util.constants import SOURCE_DIR, DATA_DIR

WORKING_DIR = os.getcwd()
WINDOWS_END = 'C:\\'
UNIX_END = '/'

def remove_handlers(logger):
    """Remove logger handlers."""
    if logger.hasHandlers():
        for handler in logger.handlers:
            logger.removeHandler(handler)

LOGGER = logging.getLogger('climada')
LOGGER.setLevel(logging.DEBUG)
LOGGER.propagate = False
remove_handlers(LOGGER)
FORMATTER = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
CONSOLE = logging.StreamHandler(stream=sys.stdout)
CONSOLE.setFormatter(FORMATTER)
LOGGER.addHandler(CONSOLE)

def check_conf():
    """Check configuration files presence and generate folders if needed."""
    for key, path in CONFIG['local_data'].items():
        abspath = path
        if not os.path.isabs(abspath):
            abspath = os.path.abspath(os.path.join(WORKING_DIR, \
                                                   os.path.expanduser(path)))
        if (key == "entity_def") and \
        ((path == "") or not os.path.isfile(abspath)):
            abspath = os.path.join(DATA_DIR, 'demo', 'entity_template.xlsx')

        if (key == "repository") and \
        ((path == "") or not os.path.isfile(abspath)):
            abspath = os.path.join(DATA_DIR)

        CONFIG['local_data'][key] = abspath

CONFIG_DIR = os.path.abspath(os.path.join(SOURCE_DIR, 'conf'))

DEFAULT_PATH = os.path.abspath(os.path.join(CONFIG_DIR, 'defaults.conf'))
if not os.path.isfile(DEFAULT_PATH):
    DEFAULT_PATH = resource_filename(Requirement.parse('climada'), \
                                     'defaults.conf')
with open(DEFAULT_PATH) as def_file:
    LOGGER.debug('Loading default config file: %s', DEFAULT_PATH)
    CONFIG = json.load(def_file)

check_conf()

def setup_logging(log_level='DEBUG'):
    """Setup logging configuration"""
    remove_handlers(LOGGER)
    LOGGER.propagate = False
    LOGGER.setLevel(getattr(logging, log_level))
    LOGGER.addHandler(CONSOLE)

def setup_conf_user():
    """Setup climada configuration"""
    conf_name = 'climada.conf'
    user_file = os.path.abspath(os.path.join(WORKING_DIR, conf_name))
    while not os.path.isfile(user_file) and user_file != UNIX_END + conf_name \
    and user_file != WINDOWS_END + conf_name:
        user_file = os.path.abspath(os.path.join(user_file, os.pardir, \
                                                 os.pardir, conf_name))

    if os.path.isfile(user_file):
        LOGGER.debug('Loading user config file: %s ...', user_file)

        with open(user_file) as conf_file:
            userconfig = json.load(conf_file)

        if 'local_data' in userconfig.keys():
            CONFIG['local_data'].update(userconfig['local_data'])

        if 'present_ref_year' in userconfig.keys():
            CONFIG['present_ref_year'] = userconfig['present_ref_year']

        if 'future_ref_year' in userconfig.keys():
            CONFIG['future_ref_year'] = userconfig['future_ref_year']

        if 'min_time_step' in userconfig.keys():
            CONFIG['tc_time_step_h'] = userconfig['tc_time_step_h']

        if 'log_level' in userconfig.keys():
            CONFIG['log_level'] = userconfig['log_level']

        check_conf()
