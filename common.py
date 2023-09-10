import os
from logger import Logger
from config import Config

PATH_ROOT = f'{os.path.expanduser("~")}/.tg_saver'
if not os.path.exists(PATH_ROOT):
    os.mkdir(PATH_ROOT)

LOG = Logger(path_log_file=f"{PATH_ROOT}/log.txt").logger
CFG = Config(path_config_file=f"{PATH_ROOT}/config.yaml")
SESSION_FILE = f"{PATH_ROOT}/session"
